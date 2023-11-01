from const import EN_REL_FREQ
from vigenere import english_alphabet

def get_blocks(text, size):
    blocks = [text[i:i+size] for i in range(0, len(text)-size, size)]
    return blocks

def get_columns(text_blocks):
    group_size = len(text_blocks[0])
    columns = []
    for letter_count in range(group_size):
        column = ''
        for group_count in range(len(text_blocks)):
            column += text_blocks[group_count][letter_count]
        columns.append(column)
    return columns

def get_letter_counts(text):
    text_upper = text.upper()
    letter_counts = {}
    for letter in english_alphabet:
        letter_counts[letter] = text_upper.count(letter)
    return letter_counts

def get_letter_frequencies(text):
    letter_counts = get_letter_counts(text)
    frequencies = {letter: count/len(text) for letter, count in letter_counts.items()}
    return frequencies

def shift(text, amount):
    shifted = ''
    for letter in text:
        shifted += english_alphabet[(english_alphabet.index(letter)-amount) % len(english_alphabet)]
    return shifted

def prob_(text, lf):
    return sum([(lf[letter]*EN_REL_FREQ[letter]) for letter in text])
  
def find_key_letter(text, lf):
    key_letter = ''
    max_corr = 0
    for count, letter in enumerate(english_alphabet):
        shifted = shift(text=text, amount=count)
        corr = prob_(text=shifted, lf=lf)
        if corr > max_corr:
            max_corr = corr
            key_letter = letter
    return key_letter

def restore_key(ciphertext, key_len):
    key = ''
    blocks = get_blocks(text=ciphertext, size=key_len)
    columns = get_columns(blocks)
    frequencies = get_letter_frequencies(text=ciphertext)
    for column in columns:
        key += find_key_letter(text=column, lf=frequencies)
    return key