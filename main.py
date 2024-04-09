from get_abstracts import extract_abstracts
from get_blacklisted_words import extract_non_infomative_words
from infomative_words import get_informative_words
from Graph_words import plot_graph
import sys

try:
    
    # Capture input file given by the user
    infile=sys.argv[1]
    
    ''' 
    Call the functions from the get_blacklisted_words.py script. This program retrieves
    blacklisted words from the abstracts present in the input file and stores them in a file.
    The program returns the absolute path of the blacklisted words file  and the number of abstracts
    '''
    print("Extracting abstracts..")
    abstracts_file_path,number_of_abstracts=extract_abstracts(infile)
    
    # Call the functions from the infomative_words.py script
    print("Blacklisting words..")
    blacklisted_words_path=extract_non_infomative_words(abstracts_file_path,number_of_abstracts)
    
    print("Procesessing infomative words.. ")
    infomative_pairs_table=get_informative_words(abstracts_file_path,blacklisted_words_path)
    
    print("Creating graph..")
    plot_graph(infomative_pairs_table)
    
    print("Completed.")
    
except IOError as err:
    print(err)
    sys.exit(1)
    
except IndexError:
    print("No input file was given. Usage:./main.py inputfile")
    sys.exit(1)