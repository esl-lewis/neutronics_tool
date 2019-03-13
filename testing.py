# TESTS

import utilities as ut
import unittest
import datetime


file_name = 'cyclemainoperationalparameters.xlsx'
# Test utilities functions

class Test_get_dates(unittest.TestCase):

    def test_get_dates_output_type(self):
        self.assertTrue(isinstance((ut.get_dates(file_name)), datetime.date))
