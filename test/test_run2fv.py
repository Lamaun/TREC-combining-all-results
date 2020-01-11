import unittest
from approvaltests import verify
import sys
import os
import imp
from mock import patch

class TestRun2Fv(unittest.TestCase):
    def test_with_imaginary_data(self):
        arguments = sys.argv + ['-i', 'test/resources/input_single_topic/',
                                '-o', '.test-output',
                                '-q', 'test/resources/test.qrel']
        with patch.object(sys, 'argv', arguments):
            imp.load_source('__main__', './run2fv.py')
            verify("".join(sorted(tuple(open('.test-output','r')))))
            os.remove('.test-output')

    def test_with_imaginary_data_for_multiple_topics(self):
        arguments = sys.argv + ['-i', 'test/resources/input_multiple_topics/',
                                '-o', '.test-output',
                                '-q', 'test/resources/test.qrel']
        with patch.object(sys, 'argv', arguments):
            imp.load_source('__main__', './run2fv.py')
            verify("".join(sorted(tuple(open('.test-output','r')))))
            os.remove('.test-output')

