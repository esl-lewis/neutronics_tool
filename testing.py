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
        dates = ut.get_dates(file_name) 
        date1 = dates[0]
        date2 = dates[1]
        check = True 
        if date1 > date2:
            check = False
        self.assertTrue(check)        
        
    def test_findrng(self):
        testdate1='2012-1-1'
        testdate2='2013-1-1'
        self.assertEqual(int(365),ut.findrng(testdate1,testdate2)) 
        
    def test_findrng_notnone(self):
        testdate1='2012-1-1'
        testdate2='2013-1-1'
        self.assertIsNotNone(ut.findrng(testdate1,testdate2))         
        
    #def test_findrng_wholenum(self):
        # check wholenum
        
if __name__ == '__main__':
    unittest.main()
