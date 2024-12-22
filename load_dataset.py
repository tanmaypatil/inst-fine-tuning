from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset
from trl import SFTConfig, SFTTrainer, setup_chat_format
import torch 

# Load a sample dataset
from datasets import load_dataset

dataset = load_dataset('json', data_files='conversation_dataset.jsonl',split="train[0:2]")

print(dataset)
print(dataset[0])
print(dataset[1])