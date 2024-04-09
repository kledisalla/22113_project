import re
import math
import os
import sys
import nltk


# Initialize Stemmer object from the Stemmer.py
try:
    
    from Stemmer import Stemmer
    stemmer=Stemmer()
    
except ModuleNotFoundError:
    print("Stemmer module not found.")
    sys.exit(1)

def tokenize_abstract(abstract):
    
    '''
    Function that tokenizes and stemms each token of an abstract
    Input: Abstract string
    Output: tuple of a list of stemmed words and the number of words
    '''
    
    # Tokenize the abstract while excluding non words and numbers
    # The regex captures also words like ATG5, FDA-Approved etc
    words = re.findall(r'\b(?:[a-zA-Z]+(?:-[a-zA-Z]+)*)+\b|\b(?:[A-Z]+[0-9/]*[-/]*[A-Z0-9/]*)+\b', abstract.lower())
    
    words=[stemmer.stem_word(word) for word in words]
    
    return words,len(words)
    
def process_abstract(tokens, blacklisted_words):
    
    '''
    Function that returns a set of stemmed words from an abstract excluding stopwords and
    non infomative words
    
    Input: List of stemmed words of an abstract, a list of non infomative words
    Output: Set of stemmed words
    '''
    
    # List of the most common stop words
    stop_words = nltk.corpus.stopwords.words('english')
    
    # Exclude stopwords and non infomative words and insert them in a set
    filtered_words = set(token for token in tokens if token not in blacklisted_words and token not in stop_words)
    
    return filtered_words

def calculate_single_word_frequencies(tokens):
    
    '''
    Function that calculates the single word frequency of words in an abstract
    Input: list of words in an abstract
    Ouput: Dictionary of word frequencies
    '''
    
    single_word_frequencies={}
    
    for token in tokens:
        if token not in single_word_frequencies:
            single_word_frequencies[token]=1
        else:
            single_word_frequencies[token]+=1
            
    return single_word_frequencies

def calculate_co_occurrence(stemmed_abstract):
    
    '''
     Function that caclulates the co-occurrence dictionary for a tokenized stemmed abstract
    
     Input: Tokenized stemmed abstract
     Output: Co-occurrence dictionary
     '''
     
    co_occurrence_frequencies = {}
    stemmed_abstract=list(stemmed_abstract)
    
    for i in range(len(stemmed_abstract)):
        
        for j in range(i + 1, len(stemmed_abstract)):
            
            word_pair = (stemmed_abstract[i], stemmed_abstract[j])
            
            if word_pair in co_occurrence_frequencies:
                co_occurrence_frequencies[word_pair] += 1
            else:
                co_occurrence_frequencies[word_pair] = 1
                
    return co_occurrence_frequencies


def calculate_log_likelihood_scores(single_word_frequencies, co_occurrence_frequencies, total_words):
    
    '''
    Function that computes the loglikelihood of pairs of words in an abstract
    Input: Single word frequencies of words in an abstract, Co-occurrence frequncies of all pairs, number of words in an abstract
    Output: Dictionary of the best pairs in an abstract with the highest log-likelihoods
    '''
    
    log_likelihood_scores = {}
    
    # Initialize a dictionary to store the maximum log likelihood score for each word1
    max_llh_for_word1 = {}
    
    for word_pair, observed_co_occurrence in co_occurrence_frequencies.items():
        word1, word2 = word_pair
        
        # Exclude words with frequencies of 1 and lower
        if single_word_frequencies[word1] > 1 and single_word_frequencies[word2] > 1:
            
            #Compute log-likelihood
            expected_co_occurrence_value = (single_word_frequencies[word1] * single_word_frequencies[word2]) / total_words
            log_likelihood = math.log(observed_co_occurrence / expected_co_occurrence_value)
            
            # Check if this is the best pair for the current word1
            if word1 not in max_llh_for_word1 or log_likelihood > max_llh_for_word1[word1][0]:
                max_llh_for_word1[word1] = (log_likelihood, word_pair)
    
    # Fill the final log_likelihood_scores dictionary with the best pairs
    for word1, (max_llh, best_pair) in max_llh_for_word1.items():
        
        log_likelihood_scores[best_pair] = max_llh
    
    return log_likelihood_scores

def get_informative_words(input_file,blacklisted_words_file):
    
    '''
    Function that processes abstracts and extracts informative words. It then
    finds the best 50 pairs of words that occurre more often the file by calculating
    the log-likelihood
    Input:File containing abstracts and a file containing blacklisted words
    Output: A file containing the best 50 pairs with the highest log-likelihood
    '''
    
    # Extract directory of the input_file
    directory, _= os.path.split(input_file)
    
    # Set the paths for the output files
    output_file= os.path.join(directory + "/", "log-likelihood_scores.txt")
    
    # Get the path for the blacklisted words
    blacklisted_words=os.path.join(directory + "/", blacklisted_words_file)
    
    # Open the blacklisted_words file and store the content in a list
    try:
        
        with open(blacklisted_words,"r", encoding="utf8") as blacklist:
            blacklisted_words=[line.strip() for line in blacklist]
            
    except IOError as err:
        print(err)
        
    # Initialize batch
    batch=20000
    
    # Initialize variables to temporarly store the current abstract being processed     
    abstract=''  
    
    # Initialize a counter to keep track of the entry being processed
    counter=0
    
    # Initliaze the dictionaries that will store the likelihood of word pairs in a batch
    total_log_likelihood_scores={}
    overall_top_100=[]
    
    entry_start_pattern = r'^(\d+): \w+.*'  # Medline entry pattern
    
    try:
        with open(input_file, "r", encoding="utf8") as infile:
            
            for line in infile:
                
                entry_line = re.match(entry_start_pattern, line)
                
                if entry_line and abstract:
                    
                    
                    # Call function to tokenize the abstract and stemm its words
                    tokenized_abstract,total_words=tokenize_abstract(abstract)
                    
                    # Call function to remove non informative words and stopwords
                    cleaned_abstract = process_abstract(tokenized_abstract, blacklisted_words) 
                    
                    # Call function to calculate single word frequencies for current abstract
                    single_word_frequencies=calculate_single_word_frequencies(tokenized_abstract)
                    
                    # Call function to calculate co-occurrence frequencies for pairs in current abstract
                    co_occurrence=calculate_co_occurrence(cleaned_abstract)
                    
                    #Call function to calculate log-likelihood for pairs in current abstract
                    log_likelihood_score=calculate_log_likelihood_scores(single_word_frequencies,co_occurrence,total_words)
                    
                    # Add log-likelihoods in total_log_likelihood_scores 
                    for pair,value in log_likelihood_score.items():
                        
                        if pair not in total_log_likelihood_scores:
                            total_log_likelihood_scores[pair]=value
                            
                        else:
                            total_log_likelihood_scores[pair]+=value
                    
                    # Check if 20,000 entries have been processed
                    if counter == batch:
                        
                        # Sort the dictionary by values in descending order
                        sorted_scores = sorted(total_log_likelihood_scores.items(), key=lambda x: x[1], reverse=True)

                        # Retain only the top 100 pairs
                        current_top_50_pairs = sorted_scores[:50]

                        # Combine current top 50 with overall top 50
                        combined_top_100 = overall_top_100 + current_top_50_pairs

                        # Convert combined_top_100 to a dictionary to remove duplicates
                        unique_pairs_dict = {}
                        
                        for pair in combined_top_100:
                            unique_pairs_dict[pair[0]] = max(unique_pairs_dict.get(pair[0], 0), pair[1])

                        # Sort the combined top 200 scores
                        overall_top_100 = sorted(unique_pairs_dict.items(), key=lambda x: x[1], reverse=True)[:50]

                        # Reset counter
                        counter = 0
                    
                    # After processing the current abstract, clear the variable for the next entry
                    abstract=''    
                    
                    #Increment the counter by 1            
                    counter+=1
                
                # If it is not a new entry, concatinate the line to the abstract variable
                else:
                    
                    abstract += line
    except IOError as err:
        print(err)
                
    try:
            # When done with all the abstracts write the top 10 pairs in a file
            with open(output_file,"w", encoding="utf8") as output:
                
                for pair in overall_top_100:
                    output.write(f"{pair}\n")      
                    
    except IOError as err:
        print(err)
        
    return output_file
        
  
   

           
                   

