import re
from context_inst_file import handle_hyphenation

def test_hypen():
    text = """ordinators are said to have links with radical Islamists in-
imical to India."""
    # Step 3: Fix hyphenated words split across lines
    text = re.sub(r'(\w+)-\s*\n*\s*(\w+)', lambda m: handle_hyphenation(m.group(1), m.group(2)), text)
    print(text)
    
   