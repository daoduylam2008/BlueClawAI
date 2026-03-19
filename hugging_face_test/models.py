from dataclasses import dataclass
from transformers import AutoTokenizer, AutoConfig


@dataclass
class ModelConfig:
    """Configuration for model-specific settings."""
    model_name: str
    pad_token: str
    pad_token_id: int
    padding_side: str
    eos_token: str
    eos_token_id: int
    vocab_size: int
    model_type: str


@dataclass
class TrainingConfig:
    """Configuration for training hyperparameters."""
    output_dir: str
    batch_size: int = 2  # Small for Mac CPU
    gradient_accumulation_steps: int = 8  # Effective batch = 16
    learning_rate: float = 2e-4
    num_train_epochs: int = 3  # Fewer epochs for speed
    max_steps: int = -1  # Use epochs
    max_seq_length: int = 1024  # Shorter = faster
    lora_r: int = 8  # Reduced LoRA rank
    lora_alpha: int = 16  # Higher alpha for better learning
    lora_dropout: float = 0.05
    save_steps: int = 100
    logging_steps: int = 10
    warmup_ratio: float = 0.05


def auto_configure_model(model_name: str, custom_pad_token: dict = None) -> ModelConfig:
    """Automatically configure model settings based on the model name."""
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    model_config = AutoConfig.from_pretrained(model_name)

    model_type = getattr(model_config, 'model_type', 'unknown')
    vocab_size = getattr(model_config, 'vocab_size', len(tokenizer.get_vocab()))

    eos_token = tokenizer.eos_token
    eos_token_id = tokenizer.eos_token_id

    if eos_token is None:
        raise ValueError(f"Model {model_name} does not have an EOS token defined.")

    pad_token = tokenizer.pad_token
    pad_token_id = tokenizer.pad_token_id

    if pad_token is None:
        if custom_pad_token is None:
            raise ValueError(f"Model {model_name} does not have a PAD token defined and no custom pad token provided.")
        pad_token = custom_pad_token
        if pad_token not in tokenizer.get_vocab():
            raise ValueError(f"Custom pad token '{pad_token}' is not in the model's vocabulary.")
        else:
            tokenizer.add_special_tokens({'pad_token': pad_token})
            pad_token_id = tokenizer.convert_tokens_to_ids(pad_token)
        
    return ModelConfig(
        model_name=model_name,
        pad_token=pad_token,
        pad_token_id=pad_token_id,
        padding_side=tokenizer.padding_side,
        eos_token=eos_token,
        eos_token_id=eos_token_id,
        vocab_size=vocab_size,
        model_type=model_type
    )


def create_training_config(model_name: str, **kwargs) -> TrainingConfig:
    """Create a training configuration with default values, allowing overrides."""
    model_clean = model_name.split('/')[-1].split('.')[-1].replace('-', '_').replace('.', '_')
    default_output_dir = f"./{model_clean}_xLAM"
    config_dict = {'output_dir': default_output_dir, **kwargs}
    return TrainingConfig(**config_dict)


