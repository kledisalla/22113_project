from Extraction import extract_abstracts
from Blacklist import extract_non_infomative_words
from Informative import get_informative_words
from Graph import plot_graph
import urllib.request
import gzip
import os
import sys

# Function that downloads and unzips the medline file
def get_file(filename=None):
    # Provide a default filename if none is provided
    if filename is None:
        filename = "pubmed_result.txt.gz"
        
    url = "https://teaching.healthtech.dtu.dk/material/22113/pubmed_result.txt.gz"
    # Extract filename from the url given
    directory = os.getcwd()
    file_path = os.path.join(directory, filename)
    
    try:
        # Check if file already exists in the current directory
        if os.path.exists(file_path):
            print(f"File found at {file_path}")
            return file_path
        
        # Ask user whether to download the file
        choice = input("File does not exist. Do you want to download it? (yes/no): ").lower()
        if choice != 'yes':
            file = input("Please input the medline file: ")
            return get_file(file)
        
        # Download the file
        print("Downloading file from", url)
        urllib.request.urlretrieve(url, file_path)
        
        # Unzip the file
        print("Unzipping file...")
        with gzip.open(file_path, 'rb') as f_in:
            with open(file_path[:-3], 'wb') as f_out:
                f_out.write(f_in.read())
        
        # Remove the gzipped file
        os.remove(file_path)
        
        print("Downloaded and extracted file to", file_path[:-3])
        
        return file_path[:-3]
    
    except Exception as e:
        print("An error occurred:", str(e))
        return None

 
try:
    
    infile=get_file(filename=None)

    print("Extracting abstracts..")
    abstracts_file_path,number_of_abstracts=extract_abstracts(infile)
    
    # Call the functions from get_blacklisted_words.py script to process the abstracts for non-informative words
    print("Blacklisting words..")
    blacklisted_words_path=extract_non_infomative_words(abstracts_file_path,number_of_abstracts)
    
    # Call the functions from get_blacklisted_words.py script to process the abstracts for informative words
    print("Procesessing infomative words.. ")
    infomative_pairs_table=get_informative_words(abstracts_file_path,blacklisted_words_path)
    
    # Call the functions from Graph_words.py to plot the infomative words
    print("Creating graph..")
    plot_graph(infomative_pairs_table)
    
    print("Completed.")
    
except IOError as err:
    print(err)
    sys.exit(1)