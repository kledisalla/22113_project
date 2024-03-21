import re
import sys

def extract_abstracts(input_file,output_file):
    ''' 
    Function that extracts the header of a medline article and its abstract.
    inputs:Pubmed file , desired output file
    '''
    
    entry_start_pattern = r'^\d+: \w+.*'
    abstract_pattern = r'^PMID: \d* +\[PubMed - indexed for MEDLINE]'
    
    # Initialize abstract count
    entry_count = 0

    # Flag to check if the previous line is empty
    prev_line_empty = True

    # Paragraph buffer that holds the last paragraph
    paragraph_buffer=''
    
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
                paragraph_buffer += line
                
            else:
                if re.match(abstract_pattern,line):
                    output_file.write(paragraph_buffer.split('\n\n')[-2] + '\n\n') 
                    paragraph_buffer = '' 
                    
                else:
                    
                    prev_line_empty = False  # Set flag to False as this line is not empty
                    paragraph_buffer += line
                    
    #Close pubmed file
    input_file.close()
    
#Main program

infile=open(sys.argv[1])
outfile=open(sys.argv[2],"w")
extract_abstracts(infile,outfile)