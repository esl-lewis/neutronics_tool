"""
This tool reads in excel data, formats appropriately and plots graph of beam
current cycles over time.
needs xlrd package
"""
import utilities as ut
import pandas as pd

file_name = 'cyclemainoperationalparameters.xlsx'

def read_excel(excel_fname):
    df = formatExcel(excel_fname)
    df = df.apply(lambda x: currentTOflux(x['Average µA']), axis=1)
    # Apply currentTOflux function down the current column
    maxlen = len(df.index)-1
    df = df.values
    # Converts to numpy friendly values
    return df, maxlen

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
    dates = ut.get_dates(file)
    start_date=dates[0]
    end_date=dates[1]

    # Find range in days between start and end points
    rng = pd.date_range(start_date, end_date, freq='D')

    # Make empty dataset
    empty_dataframe = pd.DataFrame(index=rng, columns=["Average µA"])
    empty_dataframe = empty_dataframe.fillna(0)
    
    beam_data['Dates'] = beam_data.apply(lambda x: ut.findrng(x['Start'], x['Finish']), axis=1)
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

   
if __name__ == "__main__":
    ut.setup_logging()
    df2 = formatExcel(file_name)
    # select from menu which file to load
    ut.plot_irrad(df2)
