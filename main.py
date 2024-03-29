from get_abstracts import extract_abstracts
from get_blacklisted_words import stem_text_file


infile="/home/fugen/pubmed_result.txt"
print("Extracting abstracts")
abstracts_file_path,number_of_abstracts=extract_abstracts(infile)
print("Blacklisting words")
stem_text_file(abstracts_file_path,number_of_abstracts)
