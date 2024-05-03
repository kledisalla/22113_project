import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__))[:-4])
from Extraction import extract_abstracts
from Stemmer import Stemmer
from Informative import *
 

@pytest.mark.parametrize("infile, blacklist",[("testdata/informative_test/abstract.txt", "empty_blacklist.txt"),
                                              ("testdata/informative_test/empty_infile.txt", "empty_blacklist.txt"),
                                              ("testdata/informative_test/empty_infile.txt", "blacklist.txt")])
def test_informative_with_empty_files(infile,blacklist):
    with pytest.raises(Exception):
        outfile=get_informative_words(infile,blacklist)

@pytest.mark.parametrize("infile, blacklist",[("testdata/informative_test/abstract.txt", "non_existent.txt"),
                                              ("testdata/informative_test/non_existent.txt", "blacklist.txt")])
def test_io_error(infile,blacklist):

    with pytest.raises(SystemExit) as err:
        output=get_informative_words(infile,blacklist)
        assert err.value.code == 1

        