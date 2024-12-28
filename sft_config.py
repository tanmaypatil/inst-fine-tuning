
from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset
from trl import SFTConfig, SFTTrainer, setup_chat_format
import torch

sft_config = SFTConfig(
    # Memory-critical parameters
    per_device_train_batch_size=2,  # Reduce this to save memory
    gradient_accumulation_steps=4,   # Add this to compensate for smaller batch size
    fp16=True,                      # Add this for mixed precision training
    bf16=False,                     # Alternative to fp16 for newer GPUs
    
    # Optional memory optimizations
    gradient_checkpointing=True,    # Trade computation for memory
    max_grad_norm=1.0,             # Add gradient clipping
    optim="adamw_torch",           # Choose memory-efficient optimizer
    
    # Your existing parameters
    output_dir="./sft_output",
    max_steps=1000,
    learning_rate=5e-5,
    logging_steps=10,
    save_steps=100,
    evaluation_strategy="steps",
    eval_steps=50,
    use_mps_device=(True if device == "mps" else False),
    hub_model_id=finetune_name
)