from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet, words
import enchant
from nltk.tag import pos_tag
from name_checker import *
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')


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
    validations = []
    combined = word1 + word2
    logging.info(f"combined word : {combined}") 
    word_set = set(words.words())  # Using NLTK words instead of enchant
    
    possible_forms = get_word_forms(combined)
    
    # check if it is a valid english word
    is_valid  = is_valid_english_word_ver2(combined.lower()) 
    logging.info(f" is_valid_english_word: {is_valid}") 
    if (is_valid):
      validations.append(f"Valid English word : {combined}" if is_valid else f"Invalid English word {combined}")
    
    # check if it is a name 
    checker = NameChecker()
    is_name, confidence, method = checker.is_likely_name(combined.lower())
    logging.info(f" is_likely_name: {is_name} confidence = {confidence} method ={method}")
    if (is_name == True):
      validations.append( f"Valid English name {combined}" )
    
    # Check if any word form exists in NLTK words
    nltk_word = any(form.lower() in word_set for form in possible_forms)
    logging.info(f" part of nltk_word set : {nltk_word}")
    if ( nltk_word == True):
      validations.append(f"inside nltk word set : {combined}" )
        
    # Check if any form exists in WordNet
    nltk_wordnet = any(wordnet.synsets(form) for form in possible_forms)
    logging.info(f" part of nltk_wordnet : {nltk_wordnet}")
    if ( nltk_wordnet == True):
      validations.append(f"inside nltk wordnet : {combined}" )
    
    logging.info(f"len of validations {len(validations)}")
    return len(validations) > 0, validations

def process_incorrect_words(text):
    """Clean text by joining incorrectly split words"""
    words = text.split()
    i = 0
    
    while i < len(words) - 1:
        result ,_ = validate_join(words[i], words[i+1])
        if result:
            words[i:i+2] = [''.join(words[i:i+2])]
        else:
            i += 1
    
    return ' '.join(words)

def is_valid_english_word(word):
    """
    Check if a word is valid English (including borrowed words) using multiple sources
    """
    if not word:
        return False, []
        
    word = word.lower()
    validations = []
    
    # 1. Check WordNet - most comprehensive
    if wordnet.synsets(word):
        validations.append("Found in WordNet")
    
    # 2. Check PyEnchant - includes many borrowed words
    dict_en = enchant.Dict("en_US")
    if dict_en.check(word):
        validations.append("Found in English Dictionary")
        
    # 3. Check if it's recognized as a proper noun by NLTK's POS tagger
    pos_info = pos_tag([word])
    if pos_info[0][1] in ['NNP', 'NNPS', 'NN', 'NNS']:
        validations.append(f"Recognized as {pos_info[0][1]} (noun)")
    
    # 4. Check suggested alternatives if not found
    #if not validations:
    #    suggestions = dict_en.suggest(word)
    #    if suggestions:
    #        validations.append(f"Not found. Similar words: {', '.join(suggestions[:3])}")
    
    return bool(validations), validations

def is_valid_english_word_ver2(word):
    """get the valid english word using 
       base form of the word and check if it is in wordnet
    """
    # Get base form using lemmatizer
    lemmatizer = WordNetLemmatizer()
    base_word = lemmatizer.lemmatize(word, 'v')  # Try verb form
    
    # Check original and base form
    has_synset = bool(wordnet.synsets(word)) or bool(wordnet.synsets(base_word))
    
    # Also try lemmatizing as noun in case it's not a verb
    base_noun = lemmatizer.lemmatize(word, 'n')
    has_synset = has_synset or bool(wordnet.synsets(base_noun))
    
    return has_synset


