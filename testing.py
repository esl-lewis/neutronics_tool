# TESTS

import utilities as ut
import unittest
import datetime


file_name = 'cyclemainoperationalparameters.xlsx'
# Test utilities functions


class TestUtilities(unittest.TestCase):
    
    def test_get_dates_not_none(self):
        self.assertIsNotNone(ut.get_dates(file_name))
    
    def test_get_dates_output_type(self):
        self.assertTrue((ut.get_dates(file_name)), datetime.date)
        
    #def test_get_dates_input_type(self):
    #    self.assertEqual(type(file_name),)    
        
        
if __name__ == '__main__':
    unittest.main()
