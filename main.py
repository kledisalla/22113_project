from Stemmer import Stemmer
from Extraction import extract_abstracts
from Blacklist import extract_non_informative_words
from Informative import get_informative_words
from Graph import plot_graph
import urllib.request
import gzip
import os
import sys

# Function that downloads and unzips the medline file
def get_file(filename=None):
    
    try:
        directory = os.getcwd()
        
        # Provide a default filename if none is provided
        if filename is None:
            
            filename = "pubmed_result.txt"
            zipped_file="pubmed_result.txt.gz"
            file_path = os.path.join(directory, filename)
            zipped_path= os.path.join(directory, zipped_file)
            
            if os.path.exists(file_path):
                print(f"File found at {file_path}")
                return file_path
            
            elif os.path.exists(zipped_path):
                print(f"File found at {zipped_path}")
                with gzip.open(zipped_path, 'rb') as f_in:
                    with open(zipped_path[:-3], 'wb') as f_out:
                        f_out.write(f_in.read())
                    return zipped_path[:-3]
            
            else:
                
                url = "https://teaching.healthtech.dtu.dk/material/22113/pubmed_result.txt.gz"

                # Ask user whether to download the file
                choice = input("The file required for this project does not exist. Do you want to download it? (yes/no): ").lower()
                
                while choice not in ['yes', 'no']:
                    print("Please answer with 'yes' or 'no'.")
                    choice = input("The file required for this project does not exist. Do you want to download it? (yes/no): ").lower()
                    
                if choice == 'yes':
                    
                    
                    print("Downloading file from", url)
                    filename, requested_file =urllib.request.urlretrieve(url, os.path.join(directory, os.path.basename(url)))
                    # Unzip the file
                    print("Unzipping file...")
                    
                    with gzip.open(filename, 'rb') as f_in:
                        with open(filename[:-3], 'wb') as f_out:
                            f_out.write(f_in.read())
                    
                    # Remove the gzipped file
                    os.remove(filename)
                    
                    print("Downloaded and extracted file to", directory)
                    
                    return filename[:-3]
                
                elif choice=="no":
                    
                    while True:  # Loop until a valid file is provided
                        user_input = input("Enter the path to the medline file or the gzip file: ")
                        
                        if os.path.exists(user_input):
                            file_path = os.path.abspath(user_input)
                            print("Found file")
                            if file_path.endswith(".gz"):
                                
                                unzipped_file=os.path.join(directory,file_path.split("/")[-1][:-3])
                                
                                with gzip.open(file_path, 'rb') as f_in:
                                    with open(unzipped_file, 'wb') as f_out:
                                        f_out.write(f_in.read())
                                        return unzipped_file
                            else:
                        
                                return file_path
            
                else:
                    print("Please answer with a yes or no")
                    sys.exit(1)
                    
    except gzip.BadGzipFile as e:
        print(f"Error: {e}. The file '{os.path.basename(zipped_path)}' appears to be corrupted or incomplete.")
        sys.exit(1)



def check_pair(infile,word_pair):
    try:
        if os.path.getsize(infile) == 0:
            raise Exception(" The file is empty")
        count=0
        with open(infile,"r") as llh_file:
            
            for line in llh_file:
                count+=1
                pair, llh = eval(line.strip())
                word1,word2=pair
                if (word1==word_pair[0] and word2==word_pair[1]) and count<=50:
                    return f"The word pair is in the top 50 most likely pairs with a log-likelihood of {llh}"
                elif word1==word_pair[0] and word2==word_pair[1]:
                    return f"The pair is in the top 2000 most likely pairs with a log-likelihood of {llh}"
            return "The word pair does not belong in the top 2000 most likely ones"
    except IOError as err:
        print(err)
        sys.exit(1)
 
def main():
    
    infile=get_file(filename=None)

    print("Extracting abstracts..")
    abstracts_file_path,number_of_abstracts=extract_abstracts(infile)
    
    # Call the functions from get_blacklisted_words.py script to process the abstracts for non-informative words
    print("Blacklisting words..")
    blacklisted_words_path=extract_non_informative_words(abstracts_file_path,number_of_abstracts)
    
    # Call the functions from get_blacklisted_words.py script to process the abstracts for informative words
    print("Processing informative words.. ")
    informative_pairs_table=get_informative_words(abstracts_file_path,blacklisted_words_path)
    
    # Call the functions from Graph_words.py to plot the infomative words
    print("Creating graph..")
    plot_graph(informative_pairs_table)
    
    print("Completed.")

    #Ask the user if they want to search for a pair in the final output file
    while True:
        last_choice = input("Would you like to search for a word pair? (yes/no): ").lower()
        stem=Stemmer()
        if last_choice == "yes":
            word_pair = input("Please enter a word pair: ").lower()
            word_pair=[stem.stem_word(word) for word in word_pair.split(" ")]
            print(check_pair(informative_pairs_table, word_pair))
        elif last_choice == "no":
            print("Thank you. Please check the log-likelihood_scores.txt for more information about the results")
            break
        else:
            print("Please answer with 'yes' or 'no'.")
    
if __name__=="__main__":
    main()