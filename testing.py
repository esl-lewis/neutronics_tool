 #TESTS

import utilities as ut
import unittest
import datetime


file_name = 'cyclemainoperationalparameters.xlsx'
# Test utilities functions


class TestUtilities(unittest.TestCase):
    
    # check something actually gets output
    def test_getdates_notnone(self):
        self.assertIsNotNone(ut.get_dates(file_name))
    
    # check that the result is a datetime object
    def test_getdates_outputtype(self):
        self.assertTrue((ut.get_dates(file_name)), datetime.date)
        
    def test_getdates_startbeforeend(self):
        date_start = ut.get_dates[0]
        date_end = ut.get_dates[1]
        if date_start < date_end:
            check = True
        self.assertIsTrue(check)
        
    def test_findrng_notnegative(self):
        days = ut.findrng()
        check = True 
        if days < 0:
            check = False
        self.assertIsTrue(check)
        
    def test_findrng_wholenum(self):
        # check wholenum
        
if __name__ == '__main__':
    unittest.main()
