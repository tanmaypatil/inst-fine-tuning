import json 

def test_append():
    data_to_append = {"name": "John", "age": 30}
    with open('file.jsonl', 'a') as f:
      json.dump(data_to_append, f)
      f.write('\n')  
      
def test_append2():
    data_to_append = {"name": "Jill", "age": 28}
    with open('file.jsonl', 'a') as f:
      json.dump(data_to_append, f)
      f.write('\n')  

def send_dict(name,age):
    print(f" type(name)) = {type(name)}")


def test_dict():
    data = {"name": "John", "age": 30}
    send_dict(**data)