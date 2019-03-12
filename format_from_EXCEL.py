"""
This tool reads in excel data, formats appropriately and plots graph of beam
current cycles over time.
needs xlrd package
"""
import utilities as ut



file_name = 'cyclemainoperationalparameters.xlsx'

   
if __name__ == "__main__":
    ut.setup_logging()
    df2 = ut.formatExcel(file_name)
    # select from menu which file to load
    ut.plot_irrad(df2)
