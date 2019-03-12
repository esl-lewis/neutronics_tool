# Format to CINDER
import pandas as pd
import numpy as np
import logging
from math import log10, floor
import utilities as ut

from format_from_EXCEL import formatExcel

df = formatExcel('cyclemainoperationalparameters.xlsx')

df = df.apply(lambda x: ut.currentTOflux(x['Average µA']), axis=1)

maxlen = len(df.index)-1

df = df.values
# Converts to numpy friendly values

countdays = []
flux = []

countx = 0
count0 = 0

""" Input takes integer values in days for when beam was on/off and
    the beam flux for that set of dates. This loop extracts that information
    from the  dataframe and appends it to the empty sets 'flux' and 'countdays'
"""
#  TODO
for i in range(0, maxlen):
    #if is_zero:
    #    if diff:
    #        wdas

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

# format into scientific notation
countdays = [ut.format_E(x,1) for x in countdays]

# arbitrarily chose 1.0E1 as a scaling factor
FACTOR = "1.0E1"
FACTOR0 = "0.E0"


file = open("cinder_input", "w")

# Title
file.write("(Title) Tungsten target and proton beam\n")

# Material region description
file.write("(Material region description)\n")

# Code and data library description
file.write("(Code and data library description)\n")

# Flux name
file.write("(Flux name) Proton beam flux\n")

# Material name
file.write("(Material name)Tungsten target\n")

# Number of timesteps in campaign and flux factor for all fluxes in campaign

# Timestep length and units of timestep
for i in range(0, len(countdays)):
    if flux[i] != 0.0:
        file.write("1 {}\n".format(FACTOR))
        file.write("     "+str(countdays[i])+" "+"'d'"+"\n")
    elif flux[i] == 0.0:
        file.write("1"+" "+FACTOR0+"\n")
        file.write("     "+str(countdays[i])+" "+"'d'"+"\n")

file.close()

