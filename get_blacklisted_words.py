from Stemmer import Stemmer
import random
import re
import matplotlib.pyplot as plt
import os

def random_sampling(number_of_abstracts):
    # 10% of the total
    ten_percent = int(0.10 * number_of_abstracts)
    # Sampling
    sampled_data = random.sample(range(1, number_of_abstracts + 1), ten_percent)
    return sampled_data

def word_frequency_distribution_plot(word_mapper):
    
    # Extract inner dictionary values 
    frequencies = [value for inner_dict in word_mapper.values() for value in inner_dict.values()]

    # Plot histogram with logarithmic scale on y-axis and displaying edges of bins
    
    counts, bins, _ = plt.hist(frequencies, bins=20, edgecolor='black')  # Adjust the number of bins and edgecolor as needed
    
    plt.xlabel('Word Frequency')
    plt.ylabel('Frequency Count (log scale)')
    plt.yscale('log')  # Set y-axis scale to logarithmic
    plt.title('Word Frequency Distribution (Logarithmic Scale with Bin Edges)')

    # Add annotations for bin edges
    for i in range(len(bins) - 1):
        plt.text(bins[i] + (bins[i+1] - bins[i])/2, counts[i], f'{bins[i]:.2f}', ha='center', va='bottom')
    
    # Save the plot
    plt.savefig("word_frequency_distribution.png")
    
    # Extract the threshold
    threshold_frequency = None
    
    for i in range(len(counts)):
        
        if counts[i] <= 100:
            
            threshold_frequency = bins[i]
            break
        
    return threshold_frequency
    


def stem_text_file(input_file,number_of_abstracts):
    
    directory,input_file = os.path.split(input_file)
            
    output_file= os.path.join(directory, "blacklisted_words.txt")

    # Initialize PorterStemmer object
    porter=Stemmer()
    
    entry_start_pattern = r'^(\d+): \w+.*' #Medline entry pattern
    
    #Initialize flag which denotes a new entry
    entry_flag = False

    # Open the input and output files
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        
        #Make a random sampling
        sampled_abstracts=random_sampling(number_of_abstracts)
        
        word_mapper={}
        # Process each line in the input file
        for line in infile:
            entry_line = re.match(entry_start_pattern, line)
            
            # Check if it matches the entry pattern 
            if entry_line:
                # Extract the identifier from the entry line
                entry_id = int(entry_line.group(1))
                
                # Check if the entry identifier belongs to sampled_abstracts
                if entry_id in sampled_abstracts:
                    
                    # If it does, turn the entry flag to true
                    entry_flag = True

                else:
                    # If it doesn't belong to sampled_abstracts, set entry flag to false
                    entry_flag = False
            
            # If the line is not an entry line then simply tokenize the abstract
            elif entry_flag:
                # Tokenize the line
                tokens = line.split()
                
                #Iterate over the tokens of the curent line
                for i in range(len(tokens)):
                    token = tokens[i]
                    
                    # Check with a regex if the token is a word and is not a number
                    if re.match('\w+', token) and not token.isdigit():
                        token = re.sub(r"\W", "-", token)
                        
                        # Check if the token is a part of a word like "FDA-Approved"
                        if "-" in token:
                            # In such a case split the two words and put them back to the list of tokens as separate items 
                            dash_separated_tokens = token.split("-")
                            tokens[i:i+1] = dash_separated_tokens
                        
                        # Stem the token   
                        if not tokens[i].isdigit():
                            stemmed_word = porter.stem_word(tokens[i].lower())
                            
                            # Create a key in the word_mapper dictionary with the stemmed word
                            if stemmed_word not in word_mapper:
                                
                                # and create an inner dictionary with keys as the words the stem came from
                                # and values their respective frequency
                                word_mapper[stemmed_word] = {tokens[i].lower(): 1}
                                
                            else:
                                if tokens[i].lower() not in word_mapper[stemmed_word]:
                                    
                                    word_mapper[stemmed_word][tokens[i].lower()]=1
                                    
                                else:
                                    word_mapper[stemmed_word][tokens[i].lower()]+=1
        
        # Get the threshold value
        threshold=word_frequency_distribution_plot(word_mapper)

        # Write in the output file the blacklisted words 
        for stem, inner_dict in word_mapper.items():
            
            for word in inner_dict:

                if word_mapper[stem][word]>=threshold:
                    outfile.write(word +"\n")
        

    
    



