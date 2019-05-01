 #TESTS

import utilities as ut
import unittest
import datetime
import pandas as pd
#import logging

file_name = 'cyclemainoperationalparameters.xlsx'
# Test utilities functions


class TestUtilities(unittest.TestCase):  
    #def setUp:(self):
    
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
        
    # insert funcs that test for before and after limits
          
      
    
    def test_findrng_type(self):
        testdate1='2012-1-1'
        testdate2='2013-1-1'
        self.assertIsInstance(ut.findrng(testdate1,testdate2), pd.DatetimeIndex) 
        
    def test_findrng_notnone(self):
        testdate1='2012-1-1'
        testdate2='2013-1-1'
        self.assertIsNotNone(ut.findrng(testdate1,testdate2))         
       
    def test_findrng_leapyear(self):
        testdate1='2012-1-1'
        testdate2='2013-1-1'
        rng = ut.findrng(testdate1,testdate2)
        self.assertEqual(365+2,len(rng))
        # +1 as days are counted inclusively
        # +1 more for leap year
        
    def test_findrng_year(self):
        testdate1='2013-1-1'
        testdate2='2014-1-1'
        rng = ut.findrng(testdate1,testdate2)
        self.assertEqual(365+1,len(rng))

    def test_findrng_month(self):
        testdate1='2012-1-1'
        testdate2='2012-2-1'
        rng = ut.findrng(testdate1,testdate2)
        self.assertEqual(31+1,len(rng))
    
    
    # checks that fnc adjusts date when beam was off
    def test_checkzero_beamOFFdate(self):
        start_date=datetime.datetime.strptime('2012-1-1',"%Y-%m-%d")
        file_name = 'cyclemainoperationalparameters.xlsx' 
        self.assertNotEqual(start_date,ut.check_zero(start_date,file_name))
        
    # checks that fnc does not adjust date when beam was on    
    def test_checkzero_beamONdate(self):
        start_date=datetime.datetime.strptime('2012-02-21',"%Y-%m-%d")
        file_name = 'cyclemainoperationalparameters.xlsx' 
        self.assertEqual(start_date,ut.check_zero(start_date,file_name))
       
    
    def test_validatedate_throwsexception(self):
        with self.assertRaises(ValueError):ut.validate_date('2013-ar43v1-1')
    
    
    """
    # not currently in use
    # checks that logging is setup and sends message
    def test_setuplogging_logs(self):
        with self.assertLogs('Starting irradiation history generation',level='INFO') as cm:
            logging.setup_logging
        self.assertEqual(cm.output)
    """    
        
if __name__ == '__main__':
    unittest.main()
