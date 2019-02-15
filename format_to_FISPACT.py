
"""
Formats the data from dataframe into FISPACT input file

"""

from format_from_EXCEL import formatExcel

df = formatExcel('cyclemainoperationalparameters.xlsx')


def currentTOflux(I):
    """ Converts beam current (µA) into flux
    """
    I = I/1e6  # conversion from microamps to amps
    qp = 1.6e-19  # charge of proton in Coulombs
    flux = I / (qp)
    return flux

df = df.apply(lambda x: currentTOflux(x['Average µA']), axis=1)
# Apply currentTOflux function down the current column

maxlen = len(df.index)-1

df = df.values
# Converts to numpy friendly values

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
        print('There is an error here!')

startbeamON = 0
# Checks to see if first day the beam was on or off
if df[0] > 0:
    startbeamON = True
elif df[0] == 0:
    startbeamON = False

numRuns = len(countdays)


# write to FISPACT input format
# nuclear data and intital conditions are left to user
file = open("fispact_test.i", "w")

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
