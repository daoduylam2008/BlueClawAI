from transformers import AutoModelForCausalLM, BitsAndBytesConfig
from peft import LoraConfig, prepare_model_for_kbit_training
from trl import SFTTrainer, SFTConfig
from transformers import AutoTokenizer
from datasets import Dataset

import torch
import models
import platform


def create_qlora_model(model_config: models.ModelConfig,
                       tokenizer: AutoTokenizer,
                       compute_dtype: torch.dtype,
                        attn_implementation: str) -> AutoModelForCausalLM:
    print(f"Creating QLoRA model: {model_config.model_name}")

    is_mac = platform.system() == "Darwin"

    if is_mac:
        # Mac: Use 4-bit quantization on CPU (MPS doesn't support BnB)
        print("🍎 Mac detected - using 4-bit quantization (CPU-based)")
        print("   Note: Training will be slower than GPU. Consider using smaller models.")

        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float32,
            bnb_4bit_use_double_quant=True,
        )

        model = AutoModelForCausalLM.from_pretrained(
            model_config.model_name,
            quantization_config=bnb_config,
            device_map="cpu",
            torch_dtype=torch.float32,
            trust_remote_code=True,
        )

        model = prepare_model_for_kbit_training(
            model,
            gradient_checkpointing_kwargs={'use_reentrant': True}
        )
    else:
        # Linux/Windows with GPU - full 4-bit with CUDA
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=compute_dtype,
            bnb_4bit_use_double_quant=True,
        )

        model = AutoModelForCausalLM.from_pretrained(
            model_config.model_name,
            quantization_config=bnb_config,
            device_map={"": 0},
            torch_dtype=compute_dtype,
            attn_implementation=attn_implementation,
            trust_remote_code=True,
        )

        model = prepare_model_for_kbit_training(
            model,
            gradient_checkpointing_kwargs={'use_reentrant': True}
        )

    # Configure tokenizer settings
    model.config.pad_token_id = tokenizer.pad_token_id
    model.config.use_cache = False

    return model


def create_lora_config(training_config: models.TrainingConfig) -> LoraConfig:
    # Target modules for both Llama architectures
    target_modules = [
        'k_proj', 'q_proj', 'v_proj', 'o_proj',  # Attention projections
        "gate_proj", "down_proj", "up_proj"       # Feed-forward projections
    ]

    lora_config = LoraConfig(
        lora_alpha=training_config.lora_alpha,
        lora_dropout=training_config.lora_dropout,
        r=training_config.lora_r,
        bias="none",                             # Don't adapt bias terms
        task_type="CAUSAL_LM",                   # Causal language modeling
        target_modules=target_modules
    )

    return lora_config

def train_qlora_model(dataset: Dataset,
                      model: AutoModelForCausalLM,
                      training_config: models.TrainingConfig,
                      compute_dtype: torch.dtype) -> SFTTrainer:
    # Create LoRA configuration
    peft_config = create_lora_config(training_config)

    # Remove columns that SFTTrainer will try to parse as JSON
    # Keep only 'text' which is used for training
    dataset = dataset.remove_columns([col for col in dataset.column_names if col != 'text'])

    is_mac = platform.system() == "Darwin"

    # Mac needs smaller batch sizes due to memory constraints
    if is_mac:
        batch_size = 1
        gradient_accumulation_steps = training_config.gradient_accumulation_steps * 4  # Compensate
        print("🍎 Mac detected - using memory-optimized settings")
    else:
        batch_size = training_config.batch_size
        gradient_accumulation_steps = training_config.gradient_accumulation_steps
    
    # Configure training arguments
    training_arguments = SFTConfig(
        output_dir=training_config.output_dir,
        optim="adamw_torch" if is_mac else "adamw_8bit",  # Use standard adamw on Mac
        per_device_train_batch_size=batch_size,
        gradient_accumulation_steps=gradient_accumulation_steps,
        log_level="info",                        # Detailed logging
        save_steps=training_config.save_steps,
        logging_steps=training_config.logging_steps,
        learning_rate=training_config.learning_rate,
        num_train_epochs=training_config.num_train_epochs,
        fp16=compute_dtype == torch.float16,     # Use FP16 if not using bfloat16
        bf16=compute_dtype == torch.bfloat16,    # Use bfloat16 if supported
        max_steps=training_config.max_steps,
        warmup_ratio=training_config.warmup_ratio,
        lr_scheduler_type="linear",
        dataset_text_field="text",               # Field containing training text
        max_length=training_config.max_seq_length,
        remove_unused_columns=True,              # Remove unused columns

        # Additional stability and performance settings
        dataloader_drop_last=True,               # Drop incomplete batches
        gradient_checkpointing=False,            # Disabled for faster training
        save_total_limit=1,                      # Keep only 1 checkpoint (faster)
        load_best_model_at_end=False,            # Don't load best model (saves memory)
        dataloader_pin_memory=False,             # Disable for Mac MPS
    )

    # Create trainer
    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset,
        peft_config=peft_config,
        args=training_arguments,
    )

    print(f"Training configuration:")
    print(f"   - Dataset size: {len(dataset):,} samples")
    print(f"   - Batch size: {batch_size}")
    print(f"   - Gradient accumulation: {gradient_accumulation_steps}")
    print(f"   - Effective batch size: {batch_size * gradient_accumulation_steps}")
    print(f"   - Num train epochs: {training_config.num_train_epochs}")
    print(f"   - Learning rate: {training_config.learning_rate}")
    print(f"   - Output directory: {training_config.output_dir}")

    # Start training
    print("\nBeginning training...")
    trainer.train()
    
    print("Training completed successfully!")
    
    return trainer