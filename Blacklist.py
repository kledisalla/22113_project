import random
import re
import os
import sys
import matplotlib.pyplot as plt
import nltk
nltk.download('stopwords')

def random_sampling(number_of_abstracts):
    ''' 
    Function that calculates 10% of the total number of abstracts
    and returns a list of abstract entry numbers selected at random
    Input: number of abstracts
    Output: List of randomly chosen numbers
    '''
    
    # Calculate the 10% of the total number of abstracts
    ten_percent = int(0.10 * number_of_abstracts)
    
    # Sampling
    sampled_data = random.sample(range(1, number_of_abstracts + 1), ten_percent)
    
    return sampled_data

def word_frequency_distribution_plot(word_frequencies):
    
    ''' 
    Function that creates a histogram plot with a logarithmic scale for the
    word frequencies stored in a dictionary. It returns a threshold which 
    determines which words are considered informative and which are not.
    
    Input: Dictionary of word frequencies
    Output: Threshold value
    '''
    
    # Plot histogram with logarithmic scale on y-axis and displaying edges of bins
    counts, bins, _ = plt.hist(word_frequencies.values(), bins=20, edgecolor='black')
    
    plt.xlabel('Word Frequency')
    plt.ylabel('Frequency Count (log scale)')
    plt.yscale('log') 
    plt.title('Word Frequency Distribution')

    # Add annotations for bin edges
    for i in range(len(bins) - 1):
        plt.text(bins[i] + (bins[i+1] - bins[i])/2, counts[i], f'{bins[i]:.2f}', ha='center', va='bottom')
    
    # Save the plot
    plt.savefig("word_frequency_distribution.png")
    
    # Extract the threshold
    threshold_frequency = None
    
    # Default threshold is set to 1000 or lower based on fine-tunning
    for i in range(len(counts)):
        
        if counts[i] <= 1000:
            threshold_frequency = bins[i]
            
            break
   
    return threshold_frequency
    


def extract_non_infomative_words(input_file,number_of_abstracts):
    
    ''' 
    Function that creates an output file which stores non infomative words based
    on a 10% random sampling of the total number of medline abstracts and a threhold 
    determined by logarithmic scaled histogram.
    
    Input: File containing medline abstracts with the following format:
    
    "[X]: Title.
    
     Abstract
    "
    where X is an integer
    
    Output: File containing non infomative words
    '''
    
    # Capture the full path of the directory the file containing the extracted abstracts is stored in
    # and its file name
    
    directory,filename = os.path.split(input_file)
    
    if filename=='':
        raise FileNotFoundError("File does not exist.")
        
    output_file= os.path.join(directory +"/", "blacklisted_words.txt")
    
    # List of the most common stop words
    stop_words = nltk.corpus.stopwords.words('english')

    # Initialize Stemmer object from the Stemmer.py
    try:
        
        from Stemmer import Stemmer
        stemmer=Stemmer()
        
    except ModuleNotFoundError:
        print("Stemmer module not found.")
        sys.exit(1)
    
    entry_start_pattern = r'^(\d+): \w+.*' # Medline entry pattern
    
    # Initialize flag which denotes a new entry
    entry_flag = False

    try:
        # Open the input and output files
        with open(input_file, 'r', encoding="utf8") as infile, open(output_file, 'w', encoding="utf8") as outfile:
            
            # Make a random sampling
            sampled_abstracts=random_sampling(number_of_abstracts)
            
            # Initialize a dictionary which will store the frequencies of each word in the entries after stemming
            stemmed_word_frequencies={}
            
            # Process each line in the input file
            for line in infile:
                
                # Search for the medline entry
                entry_line = re.match(entry_start_pattern, line)
                
                # Check if it matches the entry pattern 
                if entry_line:
                    
                    # Extract the identifier from the entry line
                    entry_id = int(entry_line.group(1))
                    
                    # Check if the entry identifier belongs to sampled_abstracts
                    if entry_id in sampled_abstracts:
                        
                        # If it does, turn the entry flag to True
                        entry_flag = True

                    else:
                        
                        # If it doesn't belong to sampled_abstracts, set entry flag to False
                        entry_flag = False
                
                # If the line is not an entry line then simply tokenize the abstract
                elif entry_flag:
                    
                    # Tokenize the line while excluding non words and numbers
                    # The regex captures also words like ATG5, FDA-Approved etc
                    
                    tokens = re.findall(r'\b(?:[a-zA-Z]+(?:-[a-zA-Z]+)*)+\b|\b(?:[A-Z]+[0-9/]*[-/]*[A-Z0-9/]*)+\b', line.lower())
                    
                    # Iterate over the tokens of the curent line
                    for i in range(len(tokens)):
                        
                        # Check if the current token is not a common stopword and proceed to stemming it 
                        if tokens[i] not in stop_words:
                            
                            stemmed_word = stemmer.stem_word(tokens[i])
                            
                            # Create a key in the stemmed_word_frequencies dictionary with the stemmed word
                            if stemmed_word not in stemmed_word_frequencies:
                                
                                # Set its frequency to one if it doesn't already exist in the dictionary
                                stemmed_word_frequencies[stemmed_word] = 1
                                
                            else:
                                
                                # Otherwise increment its frequency by one
                                stemmed_word_frequencies[stemmed_word] += 1
                        
            
            # Get the threshold value
            threshold=word_frequency_distribution_plot(stemmed_word_frequencies)

            # Write the non informative words in a file based on the threshold
            for word in stemmed_word_frequencies:
                if stemmed_word_frequencies[word] >=threshold:
                    outfile.write(word+"\n")

            return output_file
        
    except IOError as err:
        print(err)
        sys.exit(1)
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)
        



