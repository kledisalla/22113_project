import pytest
import sys
import os
from unittest.mock import patch
sys.path.append(os.path.dirname(os.path.realpath(__file__))[:-4])
from Blacklist import *

#Test random_sampling function where number of entries < 10
@pytest.mark.parametrize("entries",[(1)])
def test_blacklist_small_sample(entries):
    
    with pytest.raises(Exception):
        sample=random_sampling(entries)
        
#Test wrong format files
@pytest.mark.parametrize("infile,entries",[("testdata/blacklist_test/empty_medline.txt",10),("testdata/blacklist_test/no_abstract.txt",10),("testdata/blacklist_test/no_entry_line_abstracts.txt",10)])
def test_blacklist_with_wrong_format_file(infile,entries):
    with pytest.raises(Exception):
        output=extract_non_informative_words(infile,entries)
        
#Test non-existent file
def test_io_error():

    with pytest.raises(SystemExit) as err:
        abstracts,entries=extract_non_informative_words("testdata/blacklist_test/nonexistent.txt",50)
        assert err.value.code == 1

    


