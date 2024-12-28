from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet, words

# Download required NLTK data if you haven't already
# import nltk
# nltk.download('words')
# nltk.download('wordnet')

def get_word_forms(word):
    """Get different forms of a word including tenses and participles"""
    lemmatizer = WordNetLemmatizer()
    base = lemmatizer.lemmatize(word, wordnet.VERB)
    
    forms = {word, base}
    
    verb_forms = [
        base,
        base + 'ed',
        base + 'ing',
        base + 's'
    ]
    
    if base.endswith('e'):
        verb_forms.extend([
            base[:-1] + 'ing',
            base + 'd'
        ])
    
    if len(base) > 2 and base[-1] in 'bcdfghjklmnpqrstvwxz' and base[-2] in 'aeiou':
        doubled = base + base[-1]
        verb_forms.extend([
            doubled + 'ed',
            doubled + 'ing'
        ])
    
    forms.update(verb_forms)
    return forms

def validate_join(word1, word2):
    """Validate if two words should be joined using multiple checks"""
    combined = word1 + word2
    word_set = set(words.words())  # Using NLTK words instead of enchant
    
    possible_forms = get_word_forms(combined)
    
    conditions = [
        # Check if any word form exists in NLTK words
        any(form.lower() in word_set for form in possible_forms),
        
        # Check if any form exists in WordNet
        any(wordnet.synsets(form) for form in possible_forms),
        
        # Pattern checks
        len(word1) <= 3 or len(word2) <= 3,  # At least one part is short
        word1.islower() and word2.islower(),  # Both parts are lowercase
        
        # Length validation
        len(combined) < 15
    ]
    
    return sum(conditions) >= 2

def process_incorrect_words(text):
    """Clean text by joining incorrectly split words"""
    words = text.split()
    i = 0
    
    while i < len(words) - 1:
        if validate_join(words[i], words[i+1]):
            words[i:i+2] = [''.join(words[i:i+2])]
        else:
            i += 1
    
    return ' '.join(words)

