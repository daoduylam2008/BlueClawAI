import data_processing, loading_data, set_up, models

# ============ MODEL SELECTION ============
MODEL_NAME = "meta-llama/Llama-3.2-1B-Instruct"
custom_pad_token = "<|eot_id|>"

# Loading configures
model_config = models.auto_configure_model(MODEL_NAME, custom_pad_token=custom_pad_token)
training_config = models.create_training_config(MODEL_NAME)

# Tokenizer setup
tokenizer = set_up.setup_tokenizer(model_config=model_config)

# ============ DATASET ============
# ⚠️ MINIMUM 5000 SAMPLES FOR WORKING MODEL
# sample_size=5000   → ~3 hours (minimum for usable model)
# sample_size=10000  → ~6 hours (recommended)
# sample_size=50000  → ~24 hours (good quality)
dataset = data_processing.load_and_process_dataset(
    tokenizer,
    sample_size=6000,  # ⚠️ Don't go below 5000 or model won't work
    filter_empty_tools=True,
    max_length=1024
)
print(dataset)
data_processing.preview_dataset_sample(dataset, index=0)

# QLoRA model
model = loading_data.create_qlora_model(
    model_config,
    tokenizer,
    set_up.compute_dtype,
    set_up.attn_implementation
)

# Execute training
trainer = loading_data.train_qlora_model(
    dataset=dataset,
    model=model,
    training_config=training_config,
    compute_dtype=set_up.compute_dtype
)