from context_inst_gen import * 
from dotenv import load_dotenv
import re

def clean_text2(text):
    """
    Comprehensive text cleaning for PDF extracted text
    Handles headers, special characters, hyphenation, and spacing
    """
    # Step 1: Remove headers/footers
    text = re.sub(r'\d{1,2}\s+INDIA TODAY\s+[A-Z]+\s+\d{1,2},\s+\d{4}', '', text)
    
    # Step 2: Fix special characters encoding
    char_replacements = {
        'â€™': "'",
        'â€˜': "'",
        'â€œ': '"',
        'â€': '"',
        '\u2019': "'",
        '\u2018': "'",
        '\u201c': '"',
        '\u201d': '"',
        '\u2013': '-',  # en dash
        '\u2014': '-'   # em dash
    }
    for old, new in char_replacements.items():
        text = text.replace(old, new)
    
    # Step 3: Fix hyphenated words split across lines
    text = re.sub(r'(\w+)-\s*\n*\s*(\w+)', lambda m: handle_hyphenation(m.group(1), m.group(2)), text)
    
    # Step 4: Fix spacing and line breaks
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    # Step 5: Fix paragraph breaks
    # Add proper breaks after sentences that end paragraphs
    text = re.sub(r'\.(?:\s+)([A-Z])', '.\n\n\\1', text)
    
    # Step 6: Clean boilerplate content
    text = remove_boilerplate(text)
    
    # Final cleanup
    text = text.strip()
    return text

def handle_hyphenation(part1, part2):
    """
    Handle hyphenated words using general linguistic patterns rather than hardcoded lists
    """
    combined = part1 + part2
    hyphenated = part1 + '-' + part2
    
    # Rule 1: If either part is very short (1-2 chars), likely a broken word
    if len(part1) <= 2 or len(part2) <= 2:
        return combined
    
    # Rule 2: Check for compound numbers or number-word combinations
    if re.search(r'\d', hyphenated):
        return hyphenated
        
    # Rule 3: Check syllable boundaries
    # If the split occurs at a natural syllable boundary, might be intentional hyphenation
    vowels = 'aeiou'
    if (part1[-1].lower() not in vowels and 
        part2[0].lower() not in vowels):
        return combined
    
    # Rule 4: Common prefix/suffix check
    # If part1 ends with a consonant and part2 starts with vowel (or vice versa),
    # it's likely a broken word rather than intentional hyphenation
    if ((part1[-1].lower() not in vowels and part2[0].lower() in vowels) or
        (part1[-1].lower() in vowels and part2[0].lower() not in vowels)):
        return combined
        
    # Rule 5: If both parts appear to be complete words, keep hyphen
    return hyphenated


def remove_boilerplate(text):
    """Remove common magazine boilerplate text"""
    boilerplate_patterns = [
        r'FOR SUBSCRIPTION ASSISTANCE.*',
        r'SCAN HERE TO SUBSCRIBE.*',
        r'E-MAIL.*?@.*?\.com',
        r'Customer Care,.*',
        r'Readers are recommended.*?commitments.*',
        r'www\..*?\.(?:com|in)',
        r'Phone\s*/\s*Whatsapp:.*'
    ]
    
    for pattern in boilerplate_patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE | re.DOTALL)
    
    return text

def clean_text(text):
    """Clean and format PDF extracted text using natural text patterns"""
    
    # Remove header/footer type content
    text = re.sub(r'\d{1,2}\s+INDIA TODAY\s+[A-Z]+\s+\d{1,2},\s+\d{4}', '', text)
    
    # Fix special characters encoding
    char_replacements = {
        'â€™': "'",
        'â€˜': "'",
        'â€œ': '"',
        'â€': '"',
        '\u2019': "'",
        '\u2018': "'",
        '\u201c': '"',
        '\u201d': '"'
    }
    for old, new in char_replacements.items():
        text = text.replace(old, new)
    
     # Step 3: Fix hyphenated words split across lines
    text = re.sub(r'(\w+)-\s*\n*\s*(\w+)', lambda m: handle_hyphenation(m.group(1), m.group(2)), text)
   
    
    # Clean up excessive whitespace while preserving paragraph breaks
    # Look for patterns like capital letter after period and double line breaks
    sentences = text.split('. ')
    cleaned_sentences = []
    
    for sentence in sentences:
        # Remove extra spaces
        sentence = re.sub(r'\s+', ' ', sentence.strip())
        cleaned_sentences.append(sentence)
    
    # Join sentences with proper spacing
    text = '. '.join(cleaned_sentences)
    
    # Add paragraph breaks using natural indicators:
    # 1. Double line breaks in original text
    # 2. Significant topic shifts (detected by looking at sentence beginnings)
    paragraphs = []
    current_para = []
    
    for sentence in cleaned_sentences:
        if sentence:
            # Start new paragraph if:
            # - Previous sentence ended with multiple newlines
            # - Current sentence starts with transition words
            transition_patterns = r'^(However|Moreover|Furthermore|In addition|Meanwhile|Still|Thus|Therefore|As a result|Consequently|First|Second|Finally|The|This)'
            
            if (current_para and 
                (re.search(r'\n\s*\n', current_para[-1]) or 
                 re.search(transition_patterns, sentence.strip()))):
                paragraphs.append(' '.join(current_para))
                current_para = []
            
            current_para.append(sentence.strip())
    
    if current_para:
        paragraphs.append(' '.join(current_para))
    
    # Join paragraphs with double newlines
    text = '\n\n'.join(paragraphs)
    
    # Final cleanup
    text = re.sub(r'\s*\n\s*\n\s*', '\n\n', text)  # Standardize paragraph spacing
    text = text.strip()
    
    return text

'''
load_dotenv()
API_KEY = os.getenv("ANTHROPIC_API_KEY")
generator = ContextualInstructionGenerator(API_KEY)

with open('.\\extracted_text\\page_3.txt','r') as file:
    text = file.read()
    print(f"Original text:\n{text}\n")
    cf1_text = clean_text(text)
    print(f"Cleaned text:\n{cf1_text}\n")
    with open(".\\clean_text1.txt",'w') as cf1:
        cf1.write(cf1_text) 
    cf2_text = clean_text2(text)    
    with open(".\\clean_text2.txt",'w') as cf2:
        cf2.write(cf2_text) 
    


    
generator.process_text(cf1_text, 'instructions_file_new1.jsonl')

'''