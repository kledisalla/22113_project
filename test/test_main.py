import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__))[:-4])
from main import *


def test_io_error():
    infile="testdata/main_test/empty_results.txt"
    word_pair='random pair'
    with pytest.raises(Exception):
        output=check_pair(infile,word_pair)