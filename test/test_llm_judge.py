from llm_as_judge import *
from dotenv import load_dotenv
import os

def test_llm_as_judge():
    load_dotenv()
    api_key = os.getenv("OPENAI_KEY")
 
    judge = LLMJudge(api_key)   
    file_path = 'instructions_file.jsonl'
    with open(file_path, 'r', encoding='utf-8') as file:
        instruction = None 
        response = None
        for line in file:
            print(f'line is : {line}')
            if line.strip():  # Skip empty lines
                json_inst =json.loads(line)
                role = json_inst['role']
                inst_resp = json_inst['content']
                if ( role == 'user') :
                    instruction = inst_resp
                else:
                    response = inst_resp
                if (instruction != None and response != None):    
                  result = judge.evaluate(instruction, response)
                  instruction = None
                  response = None
                  print("\nSingle Evaluation Result:")
                  print(json.dumps(result.model_dump(), indent=2)) 
                
    
    
