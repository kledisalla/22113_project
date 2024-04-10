from Extraction import extract_abstracts
from Blacklist import extract_non_infomative_words
from Informative import get_informative_words
from Graph import plot_graph
import urllib.request
import gzip
import os
import sys

# Function that downloads and unzips the medline file
def get_file(url):
    
    # Extract filename from the url given
    filename = os.path.basename(url)
    directory=os.getcwd()
    
    # Check if file already exists in the current directory
    file_path = os.path.join(directory, filename)
    if os.path.exists(file_path):
        print("File already exists at", file_path)
        return file_path
    
    # Ask user whether to download the file
    choice = input("File does not exist. Do you want to download it? (yes/no): ").lower()
    if choice != 'yes':
        print("Download cancelled.")
        return None
    
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


try:
    
    #If the user didn't provide the file then call get_file function to download it
    if len(sys.argv) < 2:
        
        url = "https://teaching.healthtech.dtu.dk/material/22113/pubmed_result.txt.gz"
    
        # Call the function
        infile= get_file(url)
        
    else:
        
        # Capture input file given by the user
        infile = sys.argv[1]
   
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
    
except IndexError:
    print("No input file was given. Usage:./main.py inputfile")
    sys.exit(1)