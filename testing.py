 #TESTS

import utilities as ut
import unittest
import datetime
import pandas as pd

file_name = 'cyclemainoperationalparameters.xlsx'

class TestUtilities(unittest.TestCase):  
    
    def setUp(self):
        file_name = 'cyclemainoperationalparameters.xlsx'
    
    def test_getdates_notnone(self):
        self.assertIsNotNone(ut.get_dates(file_name))
    
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
        self.assertEqual(start_date,ut.check_zero(start_date,file_name))
       
    def test_formatExcel_output(self):
        self.assertIsInstance(ut.formatExcel(file_name),pd.DataFrame) 
    
    def test_validatedate_throwsexception(self):
        with self.assertRaises(ValueError):ut.validate_date('2013-ar43v1-1')
    
    def test_currentTOflux_1(self): 
        self.assertAlmostEqual(ut.currentTOflux(20000),1.25e17)
        
    def test_currentTOflux_2(self):
        self.assertAlmostEqual(ut.currentTOflux(0.28419),1.7761875e+12)
    
    def test_currentTOflux_3(self):
        self.assertAlmostEqual(ut.currentTOflux(0),0)
     
    def test_currentTOflux_type(self):
        self.assertIsInstance(ut.currentTOflux(0),int)
        
    def test_currentTOflux_type1(self):
        self.assertIsInstance(ut.currentTOflux(10000),float)
    
    def test_formatE_FLUKA(self):
        self.assertEqual(ut.format_E(0.000324,'FLUKA'),'3.24e-04')
    
    def test_formatE_FISPACT(self):
        self.assertEqual(ut.format_E(0.0012442,'FISPACT'),'1.2442E-03')
        
    def test_formatE_CINDER(self):
        self.assertEqual(ut.format_E(440012,'CINDER'),'4.4E+05')
    
    def test_round(self):
        self.assertEqual(ut.round_to_sf(0.0043543,3),0.00435)
        
    def test_round1(self):
        self.assertEqual(ut.round_to_sf(3532443,3),3530000)
        
    def test_round2(self):
        self.assertEqual(ut.round_to_sf(0,3),0)
    
    def test_round3(self):
        self.assertEqual(ut.round_to_sf(0.00392094,5),0.0039209)
    
if __name__ == '__main__':
    unittest.main()
