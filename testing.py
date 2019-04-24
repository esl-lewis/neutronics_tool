 #TESTS

import utilities as ut
import unittest
import datetime
import pandas as pd

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
        dates = ut.get_dates(file_name) 
        date1 = dates[0]
        date2 = dates[1]
        check = True 
        if date1 > date2:
            check = False
        self.assertTrue(check)        
      
    
    def test_findrng_type(self):
        testdate1='2012-1-1'
        testdate2='2013-1-1'
        self.assertIsInstance(ut.findrng(testdate1,testdate2), pd.DatetimeIndex) 
        
    def test_findrng_notnone(self):
        testdate1='2012-1-1'
        testdate2='2013-1-1'
        self.assertIsNotNone(ut.findrng(testdate1,testdate2))         
       
    def test_findrng_year(self):
        testdate1='2012-1-1'
        testdate2='2012-12-31'
        rng = ut.findrng(testdate1,testdate2)
        self.assertEqual(365+1,len(rng))
        # +1 as days are counted inclusively
        
        
if __name__ == '__main__':
    unittest.main()
