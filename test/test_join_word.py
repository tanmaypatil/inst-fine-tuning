from check_word_boundary import *


def test_validate_join():
    '''Simply split word - possible'''
    word1 = 'pos'
    word2 = 'sible'
    assert validate_join(word1, word2) == True

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