"""
This tool reads in excel data, formats appropriately and plots graph of beam
current cycles over time.
needs xlrd package
"""

import re
import pandas as pd
import logging
import utilities


def getdate():
    """function to select appropriate start and end date for range of
       cycles we are interested in
    """
    p = re.compile('[^0-9\s]+')
    while True:
        date = input("Please input date in the format YYYY M D \n")
        m = p.search(date)  # checks for any non numbers

        if m:
            logging.debug('Looks like you have a typo.')

        else:
            datelst = date.split()  # splits along whitespace into list of strings
            datelst = list(map(int, datelst))  # converts list of strings into list of integers
            if datelst[1] > 12 or datelst[1] <= 0:
                logging.debug('Your month looks a little funny.')
            if datelst[2] > 31 or datelst[2] <= 0:
               logging.debug('Your day value looks strange.')
            else:
                logging.debug('I work!')
                return(datelst)
        # going to have to convert this string of integers into datetime data type


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
    df = pd.read_excel(file, header=None, sheet_name='Data', skiprows=[0,1,2,3,4,5],na_values=['NA'], usecols = cols)
    df.columns = ["Start", "Finish", "Average µA"]
    df = df.drop(df.index[86:95])

    # Take start and end time for whole dataset
    # Date selectivity goes here, enter manually or select from excel file
    # check if we are in the correct range

    print("Please choose your start date")
    start_date = getdate()
    print(start_date)

    print("Please choose your end date")
    end_date = getdate()
    print(end_date)

    start_plot = pd.Timestamp(start_date[0], start_date[1], start_date[2], 0, 0, 0)
    end_plot = pd.Timestamp(end_date[0], end_date[1], end_date[2], 0, 0, 0)

    # Find range in days between start and end points
    rng = pd.date_range(start_plot, end_plot, freq='D')

    # Make empty dataset
    df0 = pd.DataFrame(index=rng, columns=["Average µA"])
    df0 = df0.fillna(0)
    
    df['Dates'] = df.apply(lambda x: findrng(x['Start'], x['Finish']), axis=1)
    """Uses findrng function on 'Start' and 'Finish' columns, creates a dataframe
    'Dates' containing a set of days spanning each cycle run.
    """

    df2 = pd.DataFrame()

    """"This loop takes each of the days in df['Dates'], matches it to its
    correct current value and appends that to our final dataframe df2.
    """
    n = 0
    for j in df.iloc[:, 3]:
        n += 1
        for i in df.iloc[n-1][3]:
            df2 = df2.append({'Average µA': df.iloc[n-1][2], 'Dates': i}, ignore_index=True)

    df2 = df2.set_index('Dates')
    """Uses dates column as index. """

    df2 = df2.combine_first(df0)
    """Ensures that empty values are set to zero through combining with an
    empty dataframe"""

    # chop data frame and only keep relevant data
    df2 = df2[start_plot:end_plot]

    return df2


if __name__ == "__main__":
    
    utilities.setup_logging()
    df2 = formatExcel('cyclemainoperationalparameters.xlsx')
    # select from menu which file to load
    utilities.plot_irrad(df2)
