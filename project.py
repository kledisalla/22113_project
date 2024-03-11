# Basic outline  of how to outline the project structure

# Project

project_folder/
│
├── data/                   # Folder to store input/output files
│   ├── accession_list.txt  # List of MEDLINE accessions
│   ├── abstracts.txt       # File containing downloaded abstracts
│   ├── blacklist.txt       # File containing non-informative words
│   └── occurrence_tables/  # Folder containing occurrence tables/data
│
├── src/                    # Folder to store Python source code
│   ├── non_informative_word_identifier.py # Program to identify non-informative words
│   ├── informative_word_extractor.py     # Program to extract informative words
│   ├── word_association_calculator.py     # Program to calculate word associations
│   └── question_answerer.py  # Program to answer questions about informative words
│
└── main.py                 # Main script to orchestrate the entire pipeline


# Scripts that could be relevant to use:

Part 1: Finding Non-informative words:

import nltk
from collections import Counter

def non_informative_word_identifier(abstractfile, outputfile, threshold = 0.05):
    with open(abstractfile, 'r') as f:
        abstract = f.read()
    
    words = nltk.word_tokenize(abstracts.lower())
    word_counts = Counter(words)
    total_words = sum(word_counts.values())

    non_informative_words = [word for word, count in word_counts.items()
                            if count / total_words > threshold]
    
    with open(outputfile, 'w') as out_f:
        out_f.write('\n'.join(non_informative_words))

abstractfile = ".txt"
outputfile = 'blacklist.txt'
non_informative_word_identifier(abstractfile, outputfile)



Part 2: Parsing abstracts and extracting informative words

import re

def informative_word_extractor(abstractfile, blacklist_file, outputfile):
    with open(abstractfile, 'r') as f:
        abstracts = f.read()

    with open(blacklist_file, 'r') as f:
        blacklist = set(f.read().splitlines())
    
    words = nltk.word_tokenize(abstracts.lower())
    informative_words = [word for word in words if word.isalpha() and word not in blacklist]

    with open(outputfile, 'w') as out_f:
        out_f.write('\n'.join(informative_words))

abstractfile =
blacklist_file =
outputfile =
informative_word_extractor(abstractfile, blacklist_file, outputfile)

# Part 3: Calculating word associations

import itertools
import math
import collections import Counter

def word_associations_calculater(abstractfile, informative_word_file, outputfile):
    with open(abstractfile, 'r') as f:
        abstracts = f.readlines()
    
    with open(informative_word_file, 'r') as f:
        informative_words = set(f.read().splitlines())

    co_occurrences = Counter()
    total_abstracts = len(abstracts)

    for abstract in abstracts:
        words = set(nltk.word_tokenize(abstract.lower()))
        informative_word_in_abstract = words.intersection(informative_words)
        for word1, word2 in itertools.combinations(informative_words_in_abstract, 2):
            co_occurrences[(word1, word2)] += 1

    with open(outputfile, 'w') as out_f:
        for (word1, word2), count in co_occurrences.items():
            expected_count = (informative_words_count[word1]*informative_words_count[word2]) / total_abstracts
            llh_score = math-log(count / expected_count)
            out_f.write(f"{word1},{word2},{count},{llh_score}\n")

    abstractfile =".txt"
    informative_words_file = ".txt"
    outputfile = ".csv"
    word_associations_calculater(abstractfile, informative_words_file, outputfile)

#Part 3: Answering questions about informative words

import pandas as pd

def find_associated_words(word, word_associations_file):
    word_associations = pd.read_csv(word_associations_file, names=["Word1", "Word2", "Count", "LLH"])
    associated_words = word_associations[word_associations['Word1'] == word]
    return associated_words

word = "cancer"
word_associations_file = "word_associations.csv"
associated_words = find_associated_words(word, word_associations_file)
print(associated_words)