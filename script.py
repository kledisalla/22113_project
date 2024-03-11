#!/usr/bin/python3
import re
import sys
import os

def get_abstracts_file(pubmed_file):
    #open the input file provided in read mode and the ouput that will be created in write mode
    with open(input_file, "r") as infile:
        try:
            with open(output_file, "w") as outfile:
                entry_found = False #Set a flag to keep track of entries
                current_entry = '' #initialize a string that stores each entry
                for line in infile:
                    #Find each entry this is done by finding the lines that start with number: 
                    if re.match("^[0-9]+:[\s\w+.]+[\s\d+\s\w+;\d].+", line.strip()):
                        entry_found = True #if found, this is a new entry so set the flag to True

                    if entry_found:
                        #If the line Related links is encountered set the flag to false, clear the current entry and write
                        #the string with the biggest length, which will always be the Abstract
                        if line.startswith("Related"):
                            outfile.write(max(current_entry.split("\n\n"), key=len) + "\n")
                            current_entry = ''
                            entry_found = False
                        else: #Else concatinate the lines till "Related links" is encountered
                            current_entry += line
        except IOError as err:
            print(err)
            
#Main program
try:
    input_file = sys.argv[1]
    output_file = os.path.splitext(input_file)[0] + "_output.txt"
    #Call function to create a file of abstracts from the input
    get_abstracts_file(input_file)
    
#If the user didn't provide an input file raise an Index error
except IndexError:
    print("Usage:./main.py <pubmed file>")
    sys.exit(1)
#If there is a issue openning the input file raise an IO error
except IOError as err:
    print(err)
    sys.exit(1)

