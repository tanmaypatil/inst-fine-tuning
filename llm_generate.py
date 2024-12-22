import json
import time
import os
from typing import List, Dict
import anthropic
from tenacity import retry, wait_exponential, stop_after_attempt
from dotenv import load_dotenv



class ConversationDatasetCreator:
    def __init__(self, api_key: str):
        self.client = anthropic.Client(api_key=api_key)

    @retry(wait=wait_exponential(multiplier=1, min=4, max=60), stop=stop_after_attempt(3))
    def generate_conversation(self, context: str) -> List[Dict]:
        """Generate a natural conversation based on the given context."""
        prompt = f"""Based on this context, create a natural conversation between a user and an assistant. The conversation should include questions and detailed responses about the topics in the context. Format it exactly as a list of dictionaries with 'role' and 'content' keys, alternating between 'user' and 'assistant' roles.

Context: {context}

Return the conversation in this exact format (a Python list of dicts):
[
    {{"role": "user", "content": "user's question"}},
    {{"role": "assistant", "content": "detailed response"}},
    {{"role": "user", "content": "follow-up question"}},
    {{"role": "assistant", "content": "detailed response"}}
]

Generate a conversation with 2-3 exchanges (4-6 messages total). Make the questions natural and the responses detailed and helpful."""

        response = self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=2000,
            temperature=0.7,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Extract and parse the conversation
        response_text = response.content[0].text
        return eval(response_text)  # Safe since we're controlling the input format

    def create_dataset(self, texts: List[str], conversations_per_text: int = 2) -> List[Dict]:
        """Create a complete conversation dataset from multiple texts."""
        dataset = []
        
        for text in texts:
            print(f"\nGenerating conversations for text: {text[:100]}...")
            for i in range(conversations_per_text):
                try:
                    conversation = self.generate_conversation(text)
                    dataset.extend(conversation)
                    print(f"Generated conversation {i+1}/{conversations_per_text}")
                    time.sleep(1)  # Rate limiting
                except Exception as e:
                    print(f"Error generating conversation: {e}")
                    continue
        
        return dataset

    def save_dataset(self, dataset: List[Dict], output_file: str, format: str = 'jsonl'):
        """Save the dataset to a file.
        
        Args:
            dataset: List of dictionaries containing the data
            output_file: Path to save the file
            format: 'json' or 'jsonl' (default: 'jsonl')
        """
        try:
            if format.lower() == 'json':
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(dataset, f, indent=4, ensure_ascii=False)
            else:  # jsonl format
                with open(output_file, 'w', encoding='utf-8') as f:
                    for item in dataset:
                        f.write(json.dumps(item, ensure_ascii=False) + '\n')
            print(f"\nDataset successfully saved to {output_file} in {format} format")
        except Exception as e:
            print(f"Error saving dataset: {e}")
def main():
    load_dotenv()
    API_KEY =  os.getenv("ANTHROPIC_API_KEY")
    
    # Sample texts (replace with your actual texts)
    texts = [
        """
        Machine Learning is a subset of artificial intelligence that enables systems to learn and improve from experience. 
        Deep Learning is a specialized form of machine learning that uses neural networks with multiple layers. 
        These technologies have revolutionized various fields including computer vision and natural language processing.
        """,
        """
        Data preprocessing is a crucial step in machine learning pipelines. It involves cleaning data, handling missing values,
        and transforming features into a format suitable for training models. Good preprocessing can significantly improve
        model performance.
        """
    ]
    
    try:
        creator = ConversationDatasetCreator(API_KEY)
        
        # Generate dataset
        dataset = creator.create_dataset(texts, conversations_per_text=2)
        
        # Save dataset
        creator.save_dataset(dataset, 'conversation_dataset.jsonl',format='jsonl')
        
        # Print sample
        print("\nSample conversations:")
        for i, item in enumerate(dataset[:4]):  # Show first two exchanges
            print(f"\n{item['role'].upper()}: {item['content'][:100]}...")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    load_dotenv()
    main()