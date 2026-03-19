from transformers import AutoTokenizer
import models
import torch
from typing import Tuple
import platform
import os


def setup_hardware_config() -> Tuple[torch.dtype, str]:
    """Automatically detect and configure hardware-specific settings."""
    is_mac = platform.system() == "Darwin"
    
    if is_mac:
        # Mac: Use CPU for 4-bit quantization (MPS doesn't support BitsAndBytes)
        print("🍎 Mac detected - will use CPU for 4-bit quantized training")
        return torch.float32, 'sdpa'
    else:
        # GPU (CUDA) settings
        if torch.cuda.is_available():
            if torch.cuda.is_bf16_supported():
                print("✅ Using CUDA with bfloat16")
                return torch.bfloat16, 'sdpa'
            else:
                print("✅ Using CUDA with float16")
                return torch.float16, 'sdpa'
        else:
            print("⚠️  No GPU available, using CPU")
            return torch.float32, 'sdpa'


def setup_tokenizer(model_config: models.ModelConfig) -> AutoTokenizer:
    """Initialize and configure the tokenizer using model configuration."""
    tokenizer = AutoTokenizer.from_pretrained(model_config.model_name, use_fast=True)

    tokenizer.pad_token = model_config.pad_token
    tokenizer.pad_token_id = model_config.pad_token_id
    tokenizer.padding_side = model_config.padding_side

    return tokenizer

# Configure hardware settings
compute_dtype, attn_implementation = setup_hardware_config()