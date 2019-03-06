"""
This tool reads in excel data, formats appropriately and plots graph of beam
current cycles over time.
needs xlrd package
"""

import re
import pandas as pd
import logging
import utilities


# now also needs to check whether one date is above or below another

import datetime


def validate_date(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect date format, should be YYYY-MM-DD")


def get_dates():
    """function to select appropriate start and end date for range of
       cycles we are interested in
    """
    date1 = input("Choose start date with format YYYY-MM-DD: ")
    validate_date(date1)
    
    date2 = input("Choose end date with format YYYY-MM-DD: ")
    validate_date(date2)
    
    
    if date1>date2:
        print("Start date is before end date. Switching them...")
        date_start = date2
        date_end = date1
    else:
        date_start = date1
        date_end = date2
    
    return [date_start,date_end]


def findrng(date1, date2):
    """
    Takes start and end date, finds the number of days between
    them.
    """
    days = pd.date_range(date1, date2, freq='D')
    return days


def formatExcel(file):
    """
    Takes data of interest in from excel file and formats to create a pandas
    dataframe. Currently acts on whole set of data.

    """
    cols = "B,C,I"
    beam_data = pd.read_excel(file, header=None, sheet_name='Data', skiprows=[0,1,2,3,4,5],na_values=['NA'], usecols = cols)
    beam_data.columns = ["Start", "Finish", "Average µA"]
    beam_data = beam_data.drop(beam_data.index[86:95])

    # Take start and end time for whole dataset
    dates = get_dates()
    start_date=datetime.datetime.strptime(dates[0], '%Y-%m-%d')
    end_date=datetime.datetime.strptime(dates[1], '%Y-%m-%d')
  

    # Find range in days between start and end points
    rng = pd.date_range(start_date, end_date, freq='D')

    # Make empty dataset
    empty_dataframe = pd.DataFrame(index=rng, columns=["Average µA"])
    empty_dataframe = empty_dataframe.fillna(0)
    
    beam_data['Dates'] = beam_data.apply(lambda x: findrng(x['Start'], x['Finish']), axis=1)
    """Uses findrng function on 'Start' and 'Finish' columns, creates a dataframe
    'Dates' containing a set of days spanning each cycle run.
    """

    final_dataframe = pd.DataFrame()

    """"This loop takes each of the days in df['Dates'], matches it to its
    correct current value and appends that to our final dataframe df2.
    """
    n = 0
    for j in beam_data.iloc[:, 3]:
        n += 1
        for i in beam_data.iloc[n-1][3]:
            final_dataframe = final_dataframe.append({'Average µA': beam_data.iloc[n-1][2], 'Dates': i}, ignore_index=True)

    final_dataframe = final_dataframe.set_index('Dates')
    """Uses dates column as index. """

    final_dataframe = final_dataframe.combine_first(empty_dataframe)
    """Ensures that empty values are set to zero through combining with an
    empty dataframe"""

    # chop data frame and only keep relevant data
    final_dataframe = final_dataframe[start_date:end_date]

    return final_dataframe

if __name__ == "__main__":
    
    utilities.setup_logging()
    df2 = formatExcel('cyclemainoperationalparameters.xlsx')
    # select from menu which file to load
    utilities.plot_irrad(df2)
