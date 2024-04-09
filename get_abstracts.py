import re
import os
import sys

def extract_abstracts(input_file):
    ''' 
    Function that extracts the header of a medline article and its abstract.
    Input: File containing medline articles
    Output: File containing the headers of the medline articles and their abstracts
    '''
    
    # Title pattern for each medline entry, i.e "1: Clin Adv Hematol Oncol. 2008 Dec;6(12):1-15."
    entry_start_pattern = r'^\d+: \w+.*'
    
    # Pattern for the ending of an entry
    ending_pattern = r'^PMID: \d* +\[PubMed - indexed for MEDLINE]'
    
    # Capture the full path of the directory where, the given by the user, input file is stored and the file name

    directory,_ = os.path.split(input_file)

    # If the absolute path of the input file was not given by the user. Meaning that it was in the same directory
    # as the script, capture the current directory so as to save the upcoming results in the same place
    
    if directory == "":
                directory = os.getcwd() +"/"
    
    # Set the name of the output file where the abstracts and headers will be saved to "abstracts.txt"     
        
    output_file_path= os.path.join(directory, "abstracts.txt")
    
    # Initialize abstract count
    entry_count = 0

    # Flag to check if the previous line is empty
    prev_line_empty = True

    # Paragraph buffer that holds the last paragraph
    paragraph_buffer=''
    
    try:
        
        with open(input_file,"r", encoding="utf8") as input_file, open(output_file_path,"w", encoding="utf8") as output_file:
            
            for line in input_file:
                
                    if re.match(entry_start_pattern, line):  # Check if line matches the starting line of an entry pattern
                        
                        entry_count += 1  # Increment abstract count
                        
                        # Check if the abstract count matches the number in the line and the previous line was empty
                        if entry_count == int(line.split(':')[0]) and prev_line_empty:
                            
                            output_file.write(line.strip() + '\n\n')  # Write the line to output file
                            
                            prev_line_empty = False  # Set flag to False since the current line is not empty
                        else:
                            entry_count -= 1  # Decrement abstract count as this line is not a new entry
                            
                    elif line.strip() == '':  # Check if the line is empty
                        
                        prev_line_empty = True  # Set flag to True
                        paragraph_buffer += line # Append the line to the current abstract 
                        
                    else:
                        
                        # If the ending pattern is found
                        if re.match(ending_pattern,line):
                            
                            # Write the current abstract in the output file 
                            output_file.write(paragraph_buffer.split('\n\n')[-2] + '\n\n') 
                            paragraph_buffer = '' # Empty the buffer for the next entry
                            
                        else:
                            
                            prev_line_empty = False  # Set flag to False as this line is not empty
                            paragraph_buffer += line # Append the line to the current abstract 
                        
        
        #Return the absolute path of the output file and the number of entries 
        return output_file_path, entry_count
            
    except IOError as err:
        print(err)
        sys.exit(1)
    
    