import json
import re
import random
from typing import List, Dict, Tuple
import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize


# Initialize NLTK and download required resources
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("Downloading required NLTK data...")
    nltk.download()
 
    
class InstructionDatasetCreator:
    def __init__(self):
        self.templates = [
            "Explain the concept of {}",
            "What is {}?",
            "Can you describe how {} works?",
            "Provide information about {}",
            "Define {}",
            "Elaborate on {}",
            "Give an overview of {}"
        ]
        
    def extract_topics(self, text: str) -> List[str]:
        """Extract potential topics from text using NLP techniques."""
        sentences = sent_tokenize(text,language="english")
        topics = []
        
        for sentence in sentences:
            # Basic noun phrase extraction (can be improved with proper NLP)
            words = word_tokenize(sentence)
            # Simple approach: look for capitalized words as potential topics
            potential_topics = [
                ' '.join(words[i:i+2]) 
                for i in range(len(words)-1) 
                if words[i][0].isupper()
            ]
            topics.extend(potential_topics)
            
        return list(set(topics))

    def create_instruction(self, topic: str) -> str:
        """Create an instruction using templates."""
        template = random.choice(self.templates)
        return template.format(topic.lower())

    def create_response(self, topic: str, text: str) -> str:
        """Create a response by finding relevant sentences."""
        sentences = sent_tokenize(text)
        relevant_sentences = []
        
        # Find sentences that mention the topic
        for sentence in sentences:
            if topic.lower() in sentence.lower():
                relevant_sentences.append(sentence)
        
        # If we found relevant sentences, combine them
        if relevant_sentences:
            response = ' '.join(relevant_sentences)
            return response
        return ""

    def create_dataset(self, raw_text: str, min_response_length: int = 50) -> List[Dict]:
        """Create instruction-response pairs from raw text."""
        dataset = []
        topics = self.extract_topics(raw_text)
        
        for topic in topics:
            instruction = self.create_instruction(topic)
            response = self.create_response(topic, raw_text)
            
            # Only add pairs with substantial responses
            if len(response) >= min_response_length:
                dataset.append({
                    "instruction": instruction,
                    "response": response,
                    "topic": topic
                })
        
        return dataset

    def save_dataset(self, dataset: List[Dict], output_file: str):
        """Save the dataset to a JSON file."""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(dataset, f, indent=2, ensure_ascii=False)

    def validate_dataset(self, dataset: List[Dict]) -> Tuple[bool, List[str]]:
        """Validate the created dataset."""
        errors = []
        for idx, item in enumerate(dataset):
            if not item.get('instruction'):
                errors.append(f"Item {idx}: Missing instruction")
            if not item.get('response'):
                errors.append(f"Item {idx}: Missing response")
            if len(item.get('response', '')) < 50:
                errors.append(f"Item {idx}: Response too short")
        
        return len(errors) == 0, errors

# Example usage
def main():
    # Sample raw text (replace with your actual text)
    raw_text = """
    Machine Learning is a subset of artificial intelligence that enables systems to learn and improve from experience. 
    Deep Learning is a specialized form of machine learning that uses neural networks with multiple layers. 
    Neural Networks are computing systems inspired by biological neural networks in animal brains.
    """
    
    creator = InstructionDatasetCreator()
    dataset = creator.create_dataset(raw_text)
    
    # Validate dataset
    is_valid, errors = creator.validate_dataset(dataset)
    if not is_valid:
        print("Dataset validation failed:")
        for error in errors:
            print(f"- {error}")
    else:
        # Save dataset
        creator.save_dataset(dataset, 'instruction_dataset.json')
        print(f"Created {len(dataset)} instruction-response pairs")
        
        # Print sample
        print("\nSample entries:")
        for item in dataset[:2]:
            print("\nInstruction:", item['instruction'])
            print("Response:", item['response'])

if __name__ == "__main__":
    main()