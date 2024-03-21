from collections import Counter
import re

def parse_abstracts(filename, blacklist):
    parsed_abstracts = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            words = re.findall(r'\b\w+\b', line.lower())
            filtered_words = [word for word in words if word not in blacklist and word.isalpha()]
            parsed_abstract = ' '.join(filtered_words)
            parsed_abstracts.append(parsed_abstract)
    return parsed_abstracts

def calculate_word_frequency(parsed_abstracts):
    word_freq = Counter()
    for abstract in parsed_abstracts:
        words = abstract.split()  # Split the abstract into words
        word_freq.update(words)  # Update word frequency counter
    return word_freq

# Replace 'abstracts_output.txt' with the path to your text file
filename = 'abstracts_output.txt'

# Replace 'blacklist.txt' with the path to your blacklisted words file
blacklist_filename = 'blacklisst.txt'

# Read the blacklist from file
with open(blacklist_filename, 'r', encoding='utf-8') as file:
    blacklist = [line.strip() for line in file]

# Parse the abstracts, disregarding blacklisted words and non-words
parsed_abstracts = parse_abstracts(filename, blacklist)

# Calculate word frequency
word_frequency = calculate_word_frequency(parsed_abstracts)

# Output the word frequency
print("Word Frequency:")
for word, frequency in word_frequency.items():
    print(f"{word}: {frequency}")
