import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__))[:-4])
from Extraction import extract_abstracts

# Test files with wrong format, or empty content
@pytest.mark.parametrize("infile",["testdata/extraction_test/empty_medline.txt", "testdata/extraction_test/no_entry_identifier_medline.txt", "testdata/extraction_test/no_pmid_line_medline.txt"])
def test_extract_abstracts_for_wrong_format_files(infile):
    
    with pytest.raises(Exception):
        
        abstracts_file,number_of_entries=extract_abstracts(infile)
        with open(abstracts_file, "r") as outfile:
            content = outfile.read()
            assert content == ''

# Test file with correct format         
@pytest.mark.parametrize("infile, output",[("testdata/extraction_test/medline.txt", "testdata/extraction_test/correct_output.txt")])            
def test_extract_abstracts_for_correct_format_files(infile,output):
    with open(output,"r") as output:
        correct_output=output.read()
    abstracts,entries=extract_abstracts(infile)
    with open(abstracts,"r") as outfile:
        content=outfile.read()
        assert content==correct_output
        assert entries==1
        
# Test reading a non-existent file      
def test_io_error():

    with pytest.raises(SystemExit) as err:
        abstracts,entries=extract_abstracts("testdata/extraction_test/nonexistent.txt")
        assert err.value.code == 1
        
    



