import spacy
import anthropic
import json
from typing import List, Dict
from tqdm import tqdm
import time
from tenacity import retry, wait_exponential, stop_after_attempt
from dotenv import load_dotenv
import os   

class ContextualInstructionGenerator:
    def __init__(self, api_key: str):
        # Initialize spaCy for text processing
        self.nlp = spacy.load("en_core_web_sm")
        self.client = anthropic.Client(api_key=api_key)
        
    def create_contextual_chunks(self, text: str, max_chunk_size: int = 2000) -> List[Dict]:
        """Create chunks while preserving context and semantic meaning."""
        doc = self.nlp(text)
        chunks = []
        current_chunk = []
        current_size = 0
        
        # Process text paragraph by paragraph
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        for para in paragraphs:
            para_doc = self.nlp(para)
            para_sentences = list(para_doc.sents)
            
            for sent in para_sentences:
                sent_text = sent.text.strip()
                sent_size = len(sent_text)
                
                # If adding this sentence would exceed chunk size
                if current_size + sent_size > max_chunk_size and current_chunk:
                    # Store current chunk with metadata
                    chunk_text = ' '.join(current_chunk)
                    chunks.append({
                        'text': chunk_text,
                        'size': current_size,
                        'topics': self.extract_topics(chunk_text)
                    })
                    # Start new chunk with overlap (last sentence)
                    current_chunk = [current_chunk[-1]] if current_chunk else []
                    current_size = len(' '.join(current_chunk))
                
                current_chunk.append(sent_text)
                current_size += sent_size
        
        # Add the last chunk if it exists
        if current_chunk:
            chunk_text = ' '.join(current_chunk)
            chunks.append({
                'text': chunk_text,
                'size': current_size,
                'topics': self.extract_topics(chunk_text)
            })
        
        return chunks

    def extract_topics(self, text: str) -> List[str]:
        """Extract main topics from text using NLP."""
        doc = self.nlp(text)
        topics = []
        
        # Extract noun phrases and named entities
        for chunk in doc.noun_chunks:
            if chunk.root.pos_ in ['NOUN', 'PROPN']:
                topics.append(chunk.text.lower())
        
        for ent in doc.ents:
            topics.append(ent.text.lower())
        
        # Remove duplicates and return
        return list(set(topics))

    @retry(wait=wait_exponential(multiplier=1, min=4, max=60), stop=stop_after_attempt(3))
    def generate_instructions(self, chunk: Dict) -> List[Dict]:
        """Generate instruction-response pairs using Claude API."""
        prompt = f"""Generate 2-3 high-quality instruction-response pairs based on this text. The instructions should be natural questions or tasks, and responses should be detailed and helpful.

Text: {chunk['text']}

Main topics: {', '.join(chunk['topics'])}

Return the pairs in this exact format (as a Python list of dicts):
[
    {{"role": "user", "content": "instruction1"}},
    {{"role": "assistant", "content": "response1"}},
    {{"role": "user", "content": "instruction2"}},
    {{"role": "assistant", "content": "response2"}}
]

Make instructions natural and varied. Responses should be detailed and based only on the provided text."""

        response = self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=2000,
            temperature=0.7,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Parse and return the response
        return eval(response.content[0].text)

    def process_text(self, text: str, output_file: str):
        """Process entire text and generate instruction dataset."""
        # Create chunks
        print("Creating contextual chunks...")
        chunks = self.create_contextual_chunks(text)
        print(f"Created {len(chunks)} chunks")
        
        # Process each chunk and save results
        with open(output_file, 'a', encoding='utf-8') as f:
            for chunk in tqdm(chunks, desc="Generating instructions"):
                try:
                    # Generate instructions for this chunk
                    instructions = self.generate_instructions(chunk)
                    
                    # Write to JSONL file
                    for item in instructions:
                        f.write(json.dumps(item, ensure_ascii=False) + '\n')
                    
                    # Rate limiting
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"Error processing chunk: {e}")
                    continue

def main():
    # Example usage
    text = """
   Just  five months ago, India viewed Bangladesh as one of its foreign policy successes. 
That changed in August when a popular rebellion ended the 15-year reign of Sheikh Hasina, and the country became a
big headache for India. 

The student-led coup wasn’t really a circus of fanaticism. Its leaders, who still advise the interim government and manage the traffic in Dhaka, avow
their faith in inclusive democracy. 
But, without doubt, the upsurge on the streets saw radical infiltration and took a nasty anti-India turn from the start. The revolution carries in its womb the danger of Islamist capture.
The first sign of trouble was that the coup violence did not just target the ruling Awami League’s symbols and
institutions. 

Attacks on Hindu homes and properties were reported from the outset. The Hindu Buddhist Christian
Unity Council (HBCUC), a minority rights group in Bangladesh, lists 2,010 communal incidents between August 5
and 20, including nine murders, 69 attacks on places of worship and four acts of violence against women. Most of
these were directed against the 13 million-strong Hindu community, which accounts for 7.95 per cent of Bangladesh’s population. 

This saw Prime Minister Narendra Modi express his concern to the new interim government headed by Nobel
laureate Muhammad Yunus, even as he became the first global leader to congratulate him on his appointment.
The Yunus government disputes the number of attacks: last week it cited 88 registered cases, and 70
arrests. Whatever the truth, there’s no doubt that Bangladesh continues to be volatile
and its Hindus live in fear and anxiety
    """
    load_dotenv()
    API_KEY = os.getenv("ANTHROPIC_API_KEY")
    generator = ContextualInstructionGenerator(API_KEY)
    generator.process_text(text, 'instructions.jsonl')

if __name__ == "__main__":
    main()