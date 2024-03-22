from Stemmer import Stemmer
import re
import sys

def stem_text_file(input_file_path, output_file_path):
    # Initialize PorterStemmer object
    porter=Stemmer()
    abstract = '' #Placeholder for the current abstract
   
    entry_start_pattern = r'^\d+: \w+.*'
    entry_flag = False

    # Open the input and output files
    with open(input_file_path, 'r') as infile, open(output_file_path, 'w') as outfile:
        
        # Process each line in the input file
        for line in infile:
            
            #Check if it matches the entry pattern 
            if re.match(entry_start_pattern, line):
                
                #if it does turn the entry flag to true
                entry_flag = True
                
                # Tokenize the previous abstract into words if it exists
                if abstract:
                    tokens= abstract.split()
                    
                    # Stem each word using the Stemmer object and write to the output file
                    for i in range(len(tokens)):
                        token=tokens[i]
                        
                        #check with a regex is the token is a word
                        if re.match('\w+', token):
                            
                            #Check if the token is a part of a word like "FDA-Apporved"
                            if "-" in token:
                                
                                #In such a case split the two words and put them back to the list of tokens are separate items 
                                dash_separated_tokens=token.split("-")
                                tokens[i:i+1]=dash_separated_tokens
                            
                            #Stem the token   
                            stemmed_word = porter.stem_word(tokens[i])
                            
                #once done, clear the previous abstract for the next entry
                abstract = ''
            #If the line is not an entry line then simply add that line to the abstract placeholder
            elif entry_flag:
                abstract += line.strip('')


#Main program
if __name__ == "__main__":
    input_file_path = sys.argv[1] 
    output_file_path = "stemmed.txt" 
    stem_text_file(input_file_path, output_file_path)
