from dotenv import load_dotenv
import os
from context_inst_gen  import *

load_dotenv()
API_KEY = os.getenv("ANTHROPIC_API_KEY")
generator = ContextualInstructionGenerator(API_KEY)


def test_gen_inst1():
    with open('.\\clean_text\\page_16.txt') as f:
      text = f.read()
      generator.process_text(text,'instructions_file_new1.jsonl')

