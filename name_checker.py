import nltk
from nltk.corpus import names
from nltk.tag import pos_tag
import re

class NameChecker:
    def __init__(self):
        # Download required NLTK data , commenting below , as actual download is interactive.
        #nltk.download('names')
        #nltk.download('averaged_perceptron_tagger')
        #nltk.download('maxent_ne_chunker')
        #nltk.download('words')
        
        # Load name datasets
        self.male_names = set(names.words('male.txt'))
        self.female_names = set(names.words('female.txt'))
        
        # Common Indian name endings
        self.indian_endings = {
            'kumar', 'raj', 'devi', 'lal', 'kant', 'wati', 'kar', 'man',
            'pal', 'deep', 'preet', 'jeet', 'nath', 'ram', 'ji', 'dev',
            'esh', 'endra', 'ani', 'ati', 'mata', 'sha', 'pri', 'van'
        }

    def is_likely_name(self, word):
        """
        Check if a word is likely to be a name using multiple methods
        Returns: tuple (is_name, confidence, method)
        """
        if not word or not isinstance(word, str):
            return False, 0, "Invalid input"
            
        # Clean the input
        word = word.strip()
        if not word:
            return False, 0, "Empty input"
            
        # Basic validation
        if not re.match(r'^[A-Za-z]+$', word):
            return False, 0, "Contains invalid characters"
            
        word = word.title()  # Convert to title case for checking
        
        # Method 1: Check against NLTK name lists
        if word in self.male_names or word in self.female_names:
            return True, 1.0, "Found in NLTK names corpus"
            
        # Method 3: Check for Indian name patterns
        for ending in self.indian_endings:
            if word.lower().endswith(ending):
                return True, 0.9, f"Matches Indian name pattern (ends with {ending})"
     
            
        return False, 0.2, "No strong indicators of being a name"
        
    def _check_name_patterns(self, word):
        """Check if word follows typical name patterns"""
        # Names typically:
        # - Start with capital letter
        # - Have reasonable length
        # - Don't have unusual character repetitions
        if not word[0].isupper():
            return False
            
        if len(word) < 2 or len(word) > 20:
            return False
            
        # Check for unusual character repetitions
        if re.search(r'(.)\1{2,}', word):  # Three or more of the same character
            return False
            
        return True

def test_name(checker, name):
    """Test a name and print results"""
    is_name, confidence, method = checker.is_likely_name(name)
    print(f"\nTesting: {name}")
    print(f"Is likely a name: {is_name}")
    print(f"Confidence: {confidence:.2f}")
    print(f"Method: {method}")

# Example usage
if __name__ == "__main__":
    checker = NameChecker()
    
    # Test cases
    test_names = [
        "Rajesh",      # Indian name
        "Smith",       # English surname
        "Priya",      # Indian name
        "Kumar",       # Indian name/surname
        "Zxywvuts",   # Random letters
        "John",        # English name
        "Ramesh",     # Indian name
        "12345",      # Invalid input
        "",           # Empty string
        "Deepak",     # Indian name
        "Williams"    # English surname
    ]
    
    for name in test_names:
        test_name(checker, name)