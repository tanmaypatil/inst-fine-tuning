from check_word_boundary import *
from name_checker import *


def test_validate_join():
    '''Simply split word - possible'''
    word1 = 'pos'
    word2 = 'sible'
    assert lambda : validate_join(word1, word2)[0] == True

def test_validate_join2():
    '''Simply split word - seemed'''
    word1 = 'see'
    word2 = 'med'
    assert validate_join(word1, word2) == True
    
def test_validate_join3():
    '''Simply split name - Mamata'''
    word1 = 'Mam'
    word2 = 'ata'
    assert validate_join(word1, word2) == True

def test_validate_name():
    ''' validate a name - Mamata'''
    checker = NameChecker()
    name = 'Mamata'
    is_name, confidence, method = checker.is_likely_name(name)
    assert is_name == True
    
def test_validate_nonname():
    '''borrowed word - Supremo'''
    word1 = 'Supr'
    word2 = 'emo'
    assert validate_join(word1, word2) == True

def test_validate_nonname2():
    '''two words - The Congress'''
    word1 = 'The'
    word2 = 'Congress'
    assert lambda: validate_join(word1, word2)[0] == False

def test_valid_eng_words():
    word = 'supremo'
    is_valid , _ = is_valid_english_word(word) 
    assert is_valid == True

    
def test_broken_words():
    '''Test broken words - from a file'''
    with open('extracted_text/page_16.txt') as f:
      for line in f:
        #print(line)
        print(f"processed line : {process_incorrect_words(line)}" )
        
def test_broken_line1():
    '''Test broken words - from line inside test code
       method is not working well
    '''
    
    line = ''' The Congress party, buoyed by its Lok Sabha gains, had all but anointed Rahul Gan dhi captain, but after the poll debacles, the crown lies uneasy Enter Mamata Ban er jee, Bengal CM and TMC supr emo, who has thrown her hat into the ring with endorse­ ments from old Maratha war h orse Sha rad Pawar and RJD patriarch Laloo Prasad Yadav
    '''
    processed_line = process_incorrect_words(line)
    print(f"processed line : {processed_line}" )
    
def test_unbroken_line2():
    line = ' The Congress party'
    processed_line = process_incorrect_words(line)
    print(f"processed line : {processed_line}" )
    
def test_broken_wordline2():
    line = 'The Congress par ty'
    processed_line = process_incorrect_words(line)
    print(f"processed line : {processed_line}" )

def test_word_forms():
    combined_word = 'TheCongress'
    possible_forms = get_word_forms(combined_word)
    print(f"possible forms : {possible_forms}")

def test_valid_english():
    word = 'theCongress'
    result,validations = is_valid_english_word(word)
    print(f"validations : {validations}")
    
def test_valid_english_ver2():
    word = 'theCongress'
    result = is_valid_english_word_ver2(word)
    print(f"result : {result}")

def test_list_len():
    val = []
    print(len(val))
    
def test_broken_word3():
    line = ' Bengal CM and TMC supr emo'
    processed_line = process_incorrect_words(line)
    print(f"processed line : {processed_line}" )
    
