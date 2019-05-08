
"""
Formats the data from dataframe into FISPACT input file

"""

import utilities as ut
import logging

from format_from_EXCEL import formatExcel


def FISPACT_output(input_file_name,output_file_name):
    
    logging.info("Reading file: %s", input_file_name)
    df, maxlen = ut.read_excel(input_file_name)

    countdays = []
    countx = 0
    count0 = 0

    flux = []

    """ FISPACT input takes integer values (here in days) for when beam was on/off
        and the beam flux for that set of dates. This loop extracts that
        information from the dataframe and appends it to the empty sets 'flux'
        and 'countdays'
    """
    for i in range(0, maxlen):
        if df[i] > 0 and (df[i]) == (df[i+1]):
            countx += 1
        elif df[i] > 0 and (df[i]) != (df[i+1]):
            countdays.append(countx)
            countx = 0
            flux.append(df[i])
        elif df[i] == 0 and (df[i]) == (df[i+1]):
            count0 += 1
        elif df[i] == 0 and (df[i]) != (df[i+1]):
            countdays.append(count0)
            count0 = 0
            flux.append(df[i])
        else:
            logging.debug('There is an error here!')

    flux = [ut.format_E(x,'FISPACT') for x in flux]


    """
    startbeamON = 0
    # Checks to see if first day the beam was on or off
    if df[0] > 0:
        startbeamON = True
    elif df[0] == 0:
        startbeamON = False
    """
    numRuns = len(countdays)
    # write to FISPACT input format
    # nuclear data and intital conditions are left to user
    ofile_name = "fispact_test.i"
    file = open(ofile_name, "w")

    file.write("<< -----get nuclear data----- >>")
    file.write("\n<< -----set initial conditions----- >>")
    file.write("\nFLUX " + str(df[0]))
    file.write("\nATOMS \nATOMS DOSE 1")

    file.write("\n<< -----irradiation phase----- >>")
    file.write("\nTIME " + str(countdays[0]))
    file.write("\nDAYS \nTAB1 41 \nATOMS")

    for j in range(1, numRuns-2):
        file.write("\nFLUX " + str(flux[j]))
        file.write("\nTIME " + str(countdays[j]) + " DAYS")
        file.write("\nATOMS")

    file.write("\n<< -----cooling phase----- >>")
    file.write("\nFLUX " + str(flux[numRuns-1]))
    file.write("\nZERO \nNOSTABLE")
    file.write("\nTIME " + str(countdays[numRuns-1]) + " DAYS")
    file.write("\nATOMS \nEND \n* END")

    file.close()
    logging.info("Writing file: %s", ofile_name)


if __name__ == "__main__":
    ut.setup_logging()
    input_file_name = 'cyclemainoperationalparameters.xlsx'
    output_file_name = 'fispact_test.i'
    FISPACT_output(input_file_name,output_file_name)
    logging.info("Completed irradiation history production")
