# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 15:13:34 2019
Title: utility functions for irrad tool

"""
from math import log10, floor
import matplotlib.pyplot as plt
import logging
import datetime
import pandas as pd



def get_dates(file_name):
    """function to select appropriate start and end date for range of
       cycles we are interested in
    """
    date1 = input("Choose start date with format YYYY-MM-DD: ")
    validate_date(date1)
    date1 = datetime.datetime.strptime(date1,"%Y-%m-%d")
    
    date2 = input("Choose end date with format YYYY-MM-DD: ")
    validate_date(date2)
    date2 = datetime.datetime.strptime(date2,"%Y-%m-%d")
    
    # this will need adjusting between datasets
    data_start_date = datetime.datetime.strptime("1998-03-25","%Y-%m-%d")
    data_end_date = datetime.datetime.now()
    
    if (date1<data_start_date) or (date2<data_start_date):
        logging.warning("Warning: Date selected is before data collection began.")
        # should be complete error, as no need to start before flux 0
        # logging instead of print warning
        # if starts on 0, jumps to the next flux non zero. 
        
    elif (date1>data_end_date) or (date2>data_end_date):
        logging.info("Date selected is after todays date.")
        # this is OK as cooling time
    
    if date1>date2:
        logging.warning("Start date is before end date. Switched them.")
        date_start = date2
        date_end = date1
    else:
        date_start = date1
        date_end = date2
       
    date_start = check_zero(date_start,file_name)
        
    
    return [date_start,date_end]


def findrng(date1, date2):
    """
    Takes start and end date, finds the number of days between
    them.
    """
    days = pd.date_range(date1, date2, freq='D')
    return days


# Check if date selected was when beam was off, if so then reset. 
def check_zero(start_date,file):
    cols = "B,C"
    beam_data = pd.read_excel(file, header=None, sheet_name='Data', skiprows=[0,1,2,3,4,5],na_values=['NA'], usecols = cols)
    beam_data.columns = ["Start", "Finish"]
    beam_data = beam_data.drop(beam_data.index[86:95])

    beam_data['Dates'] = beam_data.apply(lambda x: findrng(x['Start'], x['Finish']), axis=1)
    beam_data = beam_data['Dates']
    
    # Extract all dates the beam was on and put in list
    date_list = []
    for date_range in beam_data:
        for date in date_range:
            date_list.append(date)

    # If start_date is in this list then we have a non-zero value and nothing more needed
    beam_start_status = 'OFF'    
    for date in date_list:
        if start_date == date:
            beam_start_status = 'ON'
    print('BEAM STATUS:',beam_start_status)
    
    # If not, need to jump to next closest date in the future
    if beam_start_status == 'OFF':
        for date in date_list:
            if start_date < date:
                start_date = date
                break
        logging.warning('Start date selected was during beam off time')
        print('The next closest beam on time was selected instead.')
        print('New start date=',start_date)
        
    return start_date

    
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
    dates = get_dates(file)
    start_date=dates[0]
    end_date=dates[1]

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
    
    for counter, j in enumerate(beam_data.iloc[:, 3]):
        for i in beam_data.iloc[counter-1][3]:
            final_dataframe = final_dataframe.append({'Average µA': beam_data.iloc[counter-1][2], 'Dates': i}, ignore_index=True)

    final_dataframe = final_dataframe.set_index('Dates')
    """Uses dates column as index. """

    final_dataframe = final_dataframe.combine_first(empty_dataframe)
    """Ensures that empty values are set to zero through combining with an
    empty dataframe"""

    # Slice data frame to only keep relevant data
    final_dataframe = final_dataframe[start_date:end_date]

    return final_dataframe


def validate_date(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect date format, should be YYYY-MM-DD")

def setup_logging():
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    logging.info("Starting irradiation history generation")


def plot_irrad(df):
    """Plots beam current cycle against time."""
    plt.figure()
    x = df.index
    y = df["Average µA"]
    plt.step(x, y)


def read_excel(excel_fname):
    df = formatExcel(excel_fname)
    df = df.apply(lambda x: currentTOflux(x['Average µA']), axis=1)
    # Apply currentTOflux function down the current column
    maxlen = len(df.index)-1
    df = df.values
    # Converts to numpy friendly values
    return df, maxlen

def round_to_sf(variable, number_sigfig):
    if variable == 0:
        return 0
    else:
        return round(variable, number_sigfig-int(floor(log10(abs(variable))))-1)

def currentTOflux(I):
    """ Converts beam current (µA) into flux
    """
    I = I/1e6  # conversion from microamps to amps
    qp = 1.6e-19  # charge of proton in Coulombs
    flux = I / (qp)
    flux = round_to_sf(flux,15)
    return flux


def format_E(variable, number_sigfig,format_type):
    if variable == 0:
        return '0.0'
    elif format_type == 'FLUKA':
        return'{:.2e}'.format(variable)
    elif format_type == 'FISPACT':
        return'{:.4E}'.format(variable)
    elif format_type == 'CINDER':
        return'{:.1E}'.format(variable)
# note upper and lowercase E/e is on purpose, depends on CINDER/FLUKA/FISPACTs preferred input
