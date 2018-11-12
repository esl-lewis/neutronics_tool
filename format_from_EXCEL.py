"""
This tool reads in excel data, formats appropriately and plots graph of beam 
current cycles over time. 
needs xlrd package
"""


import pandas as pd 
import numpy as np
import datetime
import matplotlib.pyplot as plt

from pandas import ExcelWriter
from pandas import ExcelFile
 
def formatExcel(file):
    """
    Takes data of interest in from excel file and formats to create a pandas 
    dataframe. Currently acts on whole set of data. 
    
    """
    df = pd.read_excel(file, header=None, sheet_name='Data', skiprows=[0,1,2,3,4,5],na_values=['NA'], usecols = "B,C,I") 
    df.columns = ["Start","Finish","Average µA"]
    df = df.drop(df.index[86:95])

    #Take start and end time for whole dataset
    start_plot = datetime.datetime(1998, 3 ,25, 0, 0, 0)
    end_plot = datetime.datetime(2018, 3, 25, 0, 0, 0)

    #Find range between start and end for entire dataset
    rng = pd.date_range(start_plot, end_plot, freq='D')

    #Make empty dataset
    df0 = pd.DataFrame(index=rng, columns=["Average µA"])
    df0 = df0.fillna(0)

    def findrng(date1,date2):
        """
        Takes start and end date of each row, finds the range of days between
        them.
        """
        days = pd.date_range(date1, date2, freq='D')
        return days

    
    df['Dates'] = df.apply(lambda x: findrng(x['Start'], x['Finish']), axis=1)
    """Uses findrng function on 'Start' and 'Finish' columns, creates a dataframe
    'Dates' containing a set of days spanning each cycle run. 
    """

    df2 = pd.DataFrame()

    """"This loop takes each of the days in df['Dates'], matches it to its 
    correct current value and appends that to our final dataframe df2.
    """
    n=0
    for j in df.iloc[:,3]:
        n+=1
        for i in df.iloc[n-1][3]:
            df2 = df2.append({'Average µA': df.iloc[n-1][2],'Dates': i}, ignore_index=True)
        
    df2 = df2.set_index('Dates')
    """Uses dates column as index. """
    
    df2 = df2.combine_first(df0)
    """Ensures that empty values are set to zero through combining with an
    empty dataframe"""
    
    return df2


if __name__ == "__main__":
    
    df2 = formatExcel('cyclemainoperationalparameters.xlsx')
    
    """ Plots beam current cycle against time. """
    plt.figure()
    x = df2.index
    y = df2["Average µA"]
    plt.step(x,y)
    
    


