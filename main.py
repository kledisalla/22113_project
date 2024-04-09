from Extraction import extract_abstracts
from Blacklist import extract_non_infomative_words
from Informative import get_informative_words
from Graph import plot_graph
import sys

try:
    
    # Capture input file given by the user
    infile=sys.argv[1]
   
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