import re

# Copy the text to a variable
text = """
homEwork:
tHis iz your homeWork, copy these Text to variable.

You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.

last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87.
"""

# Normalize the text in terms of letter cases
normalized_text = text.lower().capitalize()

# Create a sentence with the last words of each existing sentence and add it to the end of the paragraph
sentences = re.split(r'(?<=[.!?]) +', normalized_text.strip())
last_words_sentence = ' '.join(sentence.rstrip(' .!?').split()[-1] for sentence in sentences) + '.'
normalized_text += ' ' + last_words_sentence.capitalize()

# Fix the misspelling "iz" to "is" but only when it is a mistake
corrected_text = re.sub(r'\biz\b', 'is', normalized_text)

# Calculate the number of whitespace characters in the text
whitespace_count = sum(1 for char in corrected_text if char.isspace())

print("\nNumber of whitespace characters:", whitespace_count)
