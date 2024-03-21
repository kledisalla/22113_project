from collections import Counter
import re

def calculate_word_frequency(filename):
    word_freq = Counter()
    # Read the contents of the text file
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()
        # Tokenize the text into words
        words = re.findall(r'\b\w+\b', text.lower())
        # Update word frequency counter
        word_freq.update(words)
    return word_freq

def determine_threshold_frequency(word_frequency, percentile):
    sorted_freq = sorted(word_frequency.values(), reverse=True)
    threshold_index = int(percentile * len(sorted_freq))
    threshold_frequency = sorted_freq[threshold_index]
    return threshold_frequency


def create_blacklist(word_frequency, threshold_frequency):
    # Create a blacklist of non-informative words based on the threshold frequency
    blacklist = [word for word, freq in word_frequency.items() if freq > threshold_frequency]
    return blacklist

# Replace 'abstracts_output.txt' with the path to your text file
filename = 'abstracts_output.txt'

# Calculate word frequency
word_frequency = calculate_word_frequency(filename)

# Calculate the 90th percentile threshold frequency
threshold_frequency = determine_threshold_frequency(word_frequency, 0.90)

# Create a blacklist of non-informative words
blacklist = create_blacklist(word_frequency, threshold_frequency)

# Output the blacklist
print("Blacklist of non-informative words:")
print(blacklist)
