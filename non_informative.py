import re
from collections import Counter

def is_word(word):
    # Define a regular expression pattern to match words
    word_pattern = r'^[a-zA-Z]+$'
    # Check if the word matches the pattern
    return re.match(word_pattern, word) is not None

def calculate_word_frequency(filename):
    # Read the token list from the file
    with open(filename, 'r') as file:
        token_list = [word.strip() for word in file]
    # Filter out non-words from the token list
    words = [word for word in token_list if is_word(word)]
    # Count the frequency of each word
    word_freq = Counter(words)
    return word_freq

def determine_threshold_frequency(word_frequency, total_words, percentage):
    # Calculate the threshold frequency based on the desired percentage
    threshold_frequency = int(total_words * percentage)
    return threshold_frequency

def create_blacklist(word_frequency, threshold_frequency):
    # Create a blacklist of non-informative words based on the threshold frequency
    blacklist = [(word, freq) for word, freq in word_frequency.items() if freq > 1000 and freq <= threshold_frequency]
    return blacklist

def write_blacklist_to_file(blacklist, output_filename):
    # Write the blacklist to the output file
    with open(output_filename, 'w') as file:
        for word, freq in blacklist:
            file.write(f"{word}: {freq}\n")

# Specify the filename of the token list
filename = 'stemmed_abstracts.txt'

# Calculate word frequency
word_frequency = calculate_word_frequency(filename)

# Calculate total number of words in the token list
total_words = sum(word_frequency.values())

# Determine the threshold frequency (90% of total words)
threshold_frequency = determine_threshold_frequency(word_frequency, total_words, 0.90)

# Create a blacklist of non-informative words with their frequencies
blacklist = create_blacklist(word_frequency, threshold_frequency)

# Output the blacklist to a file
output_filename = 'blacklist.txt'
write_blacklist_to_file(blacklist, output_filename)

print("Blacklist of non-informative words has been written to", output_filename)
