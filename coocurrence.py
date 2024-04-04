import numpy as np
import itertools
import math
from scipy import sparse

# Step 1: Read and tokenize informative words
with open('informative_words.txt', 'r') as file:
    informative_words = file.read().split()

# Step 2: Create co-occurrence matrix (sparse representation)
window_size = 5  # Adjust as needed
co_occurrence_matrix = sparse.lil_matrix((len(informative_words), len(informative_words)), dtype=int)

with open('your_text_file.txt', 'r') as file:  # Replace 'your_text_file.txt' with the actual text file
    for line in file:
        tokens = line.split()
        for i, word in enumerate(tokens):
            if word in informative_words:
                start = max(0, i - window_size)
                end = min(len(tokens), i + window_size + 1)
                context = tokens[start:end]
                context.remove(word)  # Remove the target word from its own context
                for context_word in context:
                    if context_word in informative_words:
                        co_occurrence_matrix[informative_words.index(word), informative_words.index(context_word)] += 1

co_occurrence_matrix = co_occurrence_matrix.tocsr()

# Step 3: Calculate log-likelihood score
def log_likelihood_score(co_occurrence_matrix, word1_index, word2_index):
    # Implementation remains the same

# Calculate log-likelihood score for each word pair
association_strengths = {}
for i, j in itertools.combinations(range(len(informative_words)), 2):
    word1 = informative_words[i]
    word2 = informative_words[j]
    score = log_likelihood_score(co_occurrence_matrix, i, j)
    association_strengths[(word1, word2)] = score

# Sort association strengths
sorted_association_strengths = sorted(association_strengths.items(), key=lambda x: x[1], reverse=True)

# Print the results
for pair, score in sorted_association_strengths:
    print(f"Word pair: {pair}, Log-likelihood score: {score}")





####### PART 2 #######
    
import numpy as np

def compute_co_occurrence(word_pairs, abstracts):
    co_occurrence_matrix = np.zeros((len(word_pairs), len(word_pairs)))
    
    for abstract in abstracts:
        for i, word1 in enumerate(word_pairs):
            for j, word2 in enumerate(word_pairs):
                if word1 != word2 and word1 in abstract and word2 in abstract:
                    co_occurrence_matrix[i][j] += 1
                    
    return co_occurrence_matrix

def compute_log_likelihood(co_occurrence_matrix, word_freq, total_words):
    log_likelihood_scores = np.zeros_like(co_occurrence_matrix, dtype=float)
    
    for i in range(len(co_occurrence_matrix)):
        for j in range(len(co_occurrence_matrix)):
            if i != j:
                expected_co_occurrence = (word_freq[i] * word_freq[j]) / total_words
                observed_co_occurrence = co_occurrence_matrix[i][j]
                
                log_likelihood_scores[i][j] = np.log(observed_co_occurrence / expected_co_occurrence)
                
    return log_likelihood_scores

# Example usage:
word_pairs = ["word1", "word2", "word3"]  # Replace with your actual word pairs
abstracts = [...]  # List of abstracts, each represented as a list of words

# Calculate co-occurrence matrix
co_occurrence_matrix = compute_co_occurrence(word_pairs, abstracts)

# Compute log-likelihood scores
word_freq = [...]  # List of frequencies of each word in word_pairs
total_words = [...]  # Total number of words in the abstracts
log_likelihood_scores = compute_log_likelihood(co_occurrence_matrix, word_freq, total_words)
