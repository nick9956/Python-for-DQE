import re

# Copy the text to a variable
def get_text():
    return """
homEwork:
tHis iz your homeWork, copy these Text to variable.

You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.

last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87.
"""

# Normalize the text in terms of letter cases
def normalize_text(text):
    return text.lower().capitalize()

# Create a sentence with the last words of each existing sentence and add it to the end of the paragraph
def add_last_words_sentence(text):
    sentences = re.split(r'(?<=[.!?]) +', text.strip())
    last_words_sentence = ' '.join(sentence.rstrip(' .!?').split()[-1] for sentence in sentences) + '.'
    return text + ' ' + last_words_sentence.capitalize()

# Fix the misspelling "iz" to "is" but only when it is a mistake
def fix_misspellings(text):
    return re.sub(r'\biz\b', 'is', text)

# Calculate the number of whitespace characters in the text
def count_whitespace(text):
    return len(re.findall(r'\s', text))

# Main function to execute all steps
def process_text():
    text = get_text()
    text = normalize_text(text)
    text = add_last_words_sentence(text)
    text = fix_misspellings(text)
    whitespace_count = count_whitespace(text)

    print("\nNumber of whitespace characters:", whitespace_count)

# Execute the main function
process_text()
