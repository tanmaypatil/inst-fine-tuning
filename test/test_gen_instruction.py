from dotenv import load_dotenv
import os
from context_inst_gen  import *
from file_util import *

load_dotenv()
API_KEY = os.getenv("ANTHROPIC_API_KEY2")
generator = ContextualInstructionGenerator(API_KEY)


def test_gen_inst2():
    with open('.\\extracted_text\\page_16.txt') as f:
      text = f.read()
      generator.process_text(text,'instructions_file_new1.jsonl')
      
def test_gen_inst_all():
    file_paths = list_files_with_extension('.\\extracted_text','.txt')
    print(f'Number of files: {len(file_paths)}')
    for file_path in file_paths:
        with open(f".\\extracted_text\\{file_path}","r",encoding="utf-8") as f:
            print(f"Processing file: {file_path}")
            text = f.read()
            generator.process_text(text,'instructions_file_all.jsonl')
    
