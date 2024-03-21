import re
from collections import Counter

def is_word(word):
    # Define a regular expression pattern to match words
    word_pattern = r'^[a-zA-Z]+$'
    # Check if the word matches the pattern
    return re.match(word_pattern, word) is not None

def load_abstracts(filename):
    # Read the abstracts from the file
    with open(filename, 'r') as file:
        abstracts = file.readlines()
    return abstracts

def remove_blacklisted_and_non_words(abstracts, blacklist):
    filtered_abstracts = []
    for abstract in abstracts:
        # Tokenize the abstract into words
        words = re.findall(r'\b\w+\b', abstract.lower())
        # Remove blacklisted words and non-words
        filtered_words = [word for word in words if word not in blacklist and is_word(word)]
        # Collapse multiple occurrences of the same word within an abstract
        filtered_abstract = ' '.join(filtered_words)
        filtered_abstracts.append(filtered_abstract)
    return filtered_abstracts

def calculate_word_frequency(abstracts):
    # Combine all abstracts into a single text
    all_text = ' '.join(abstracts)
    # Tokenize the text into words
    words = re.findall(r'\b\w+\b', all_text.lower())
    # Count the frequency of each word
    word_freq = Counter(words)
    return word_freq

def extract_informative_words(word_frequency, threshold_value):
    # Extract informative words based on their frequency and relevance
    informative_words = [(word, freq) for word, freq in word_frequency.items() if freq < threshold_value]
    return informative_words

def write_informative_words_to_file(informative_words, output_filename):
    # Write the informative words to the output file
    with open(output_filename, 'w') as file:
        for word, freq in informative_words:
            file.write(f"{word}: {freq}\n")

# Specify the filenames
abstracts_filename = 'abstracts_assembled.txt'
blacklist_filename = 'blacklist.txt'
output_filename = 'informative_words.txt'

# Load the blacklisted words
with open(blacklist_filename, 'r') as file:
    blacklist = {word.strip(): True for word in file}

# Load and preprocess the abstracts
abstracts = load_abstracts(abstracts_filename)
filtered_abstracts = remove_blacklisted_and_non_words(abstracts, blacklist)

# Calculate word frequency
word_frequency = calculate_word_frequency(filtered_abstracts)

# Determine the threshold frequency (e.g., 1000 times)
threshold_value = 1000

# Extract informative words based on their frequency and relevance
informative_words = extract_informative_words(word_frequency, threshold_value)

# Write the informative words to the output file
write_informative_words_to_file(informative_words, output_filename)

print("Informative words have been written to", output_filename)
