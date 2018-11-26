# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 13:53:44 2018

@author: fhs33517
"""

#FORMAT TO FLUKA
import re
import pandas as pd 
import numpy as np
import datetime
import matplotlib.pyplot as plt

from pandas import ExcelWriter
from pandas import ExcelFile
from math import log10, floor
 

from format_from_EXCEL import formatExcel

df = formatExcel('cyclemainoperationalparameters.xlsx')

def currentTOflux(I):
    """ Converts beam current (µA) into flux
    """
    I = I/1e6 #conversion from microamps to amps
    qp = 1.6e-19 # charge of proton in Coulombs  
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

""" FISPACT input takes integer values (here in days) for when beam was on/off and 
the beam flux for that set of dates. This loop extracts that information from the
dataframe and appends it to the empty sets 'flux' and 'countdays'
"""
for i in range(0,maxlen):
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

# convert days into seconds
countdays = [x * 24 * 60 * 60 for x in countdays]

# round down both flux and second values to 3 sf
def round_to_4sf(x):
    """ note, change value in front of int to change no. of sfs we round to
    """
    if x == 0:
        return 0
    else:
        return round(x, 4-int(floor(log10(abs(x))))-1)

countdays = list(map(round_to_4sf, countdays))
flux = list(map(round_to_4sf, flux))

# convert flux into scientific notation 
def format_E(x):
    if x == 0:
        return '0.0'
    else:
        return'{:.2e}'.format(x)    

flux = list(map(format_E, flux))

        

print(countdays)
print(flux)

print(type(flux[0]))
print(type(flux[1]))
# changes 0.0 to 0, need to change back


startbeamON = 0
#Checks to see if first day the beam was on or off
if flux[0] == '0.0':
    startbeamON = False
else:
    startbeamON = True

print(startbeamON)

tot = len(countdays) 

#write to FLUKA file
file = open("fluka_test.i","w")
#All of these conditionals are to satisfy FLUKAS input requirements.
#Beam must flicker ON then OFF 

for i in range(0,(tot)):
    print(i)
    if i == 0 and startbeamON == True:
        # 0 = on, even == on
        file.write("\n* Beam ON: " + str(countdays[i]) +" seconds,Beam OFF: "+ str(countdays[i+1]))
        file.write(" seconds,Beam ON: "+str(countdays[i+2])+"\n")
        
        file.write("IRRPROFI   "+str(countdays[i])+". "+str(flux[i])+" ")
    
    elif i == 0 and startbeamON == False:
        # 0 = off, even == off
        file.write("\n* Beam OFF: " + str(countdays[i]) +" seconds,Beam ON: "+ str(countdays[i+1]))
        file.write(" seconds,Beam OFF: "+str(countdays[i+2])+"\n")
        
        file.write("IRRPROFI   "+str(countdays[i])+". "+str(flux[i])+" ")
    
    
    # for the end bits
    elif tot % 3 == 1 and i == tot - 1:
        if i % 2 == 0 and startbeamON == True:
            file.write("\n* Beam ON: " + str(countdays[i]))
            file.write("IRRPROFI   "+str(countdays[i])+". "+str(flux[i])+" ")
        
        elif i % 2 != 0 and startbeamON == True:
            file.write("\n* Beam OFF: " + str(countdays[i]))
            file.write("IRRPROFI   "+str(countdays[i])+". "+str(flux[i])+" ")
                
        elif i % 2 == 0 and startbeamON == False:
            file.write("\n* Beam OFF: " + str(countdays[i]))
            file.write("IRRPROFI   "+str(countdays[i])+". "+str(flux[i])+" ")
          
        elif i % 2 != 0 and startbeamON == False:
            file.write("\n* Beam ON: " + str(countdays[i]))
            file.write("\nIRRPROFI   "+str(countdays[i])+". "+str(flux[i])+" ")
        
        
            
    elif tot % 3 == 2 and i == tot - 2: 
        if i % 2 == 0 and startbeamON == True:
            file.write("\n* Beam OFF: " + str(countdays[i]) +" seconds,Beam ON: "+ str(countdays[i+1]))
            file.write("\nIRRPROFI   "+str(countdays[i])+". "+str(flux[i])+" "+str(countdays[i+1])+"."+str(flux[i+1])+" ")
        elif i % 2 != 0 and startbeamON == True:
            file.write("\n* Beam OFF: " + str(countdays[i]) +" seconds,Beam ON: "+ str(countdays[i+1]))
            file.write("\nIRRPROFI   "+str(countdays[i])+". "+str(flux[i])+" "+str(countdays[i+1])+"."+str(flux[i+1])+" ")
        elif i % 2 == 0 and startbeamON == False:
            file.write("\n* Beam ON: " + str(countdays[i]) +" seconds,Beam OFF: "+ str(countdays[i+1]))
            file.write("\nIRRPROFI   "+str(countdays[i])+". "+str(flux[i])+" "+str(countdays[i+1])+"."+str(flux[i+1])+" ")
        elif i % 2 != 0 and startbeamON == False:
            file.write("\n* Beam ON: " + str(countdays[i]) +" seconds,Beam OFF: "+ str(countdays[i+1]))
            file.write("\nIRRPROFI   "+str(countdays[i])+". "+str(flux[i])+" "+str(countdays[i+1])+". "+str(flux[i+1])+" ")
    
    
    elif tot % 3 == 0 and i == tot - 3:
        if i % 2 == 0 and startbeamON == True:
            file.write("\n* Beam ON: " + str(countdays[i]) +" seconds,Beam OFF: "+ str(countdays[i+1])+" seconds,Beam ON: "+str(countdays[i+2])+"\n")
            file.write("\nIRRPROFI   "+str(countdays[i])+". "+str(flux[i])+" "+str(countdays[i+1])+"."+str(flux[i+1])+" "+str(countdays[i+2])+"."+str(flux[i+2]))
        elif i % 2 != 0 and startbeamON == True:
           file.write("\n* Beam OFF: " + str(countdays[i]) +" seconds,Beam ON: "+ str(countdays[i+1])+" seconds,Beam OFF: "+str(countdays[i+2])+"\n")
           file.write("\nIRRPROFI   "+str(countdays[i])+". "+str(flux[i])+" "+str(countdays[i+1])+"."+str(flux[i+1])+" "+str(countdays[i+2])+"."+str(flux[i+2]))
        elif i % 2 == 0 and startbeamON == False:
            file.write("\n* Beam OFF: " + str(countdays[i]) +" seconds,Beam ON: "+ str(countdays[i+1])+" seconds,Beam OFF: "+str(countdays[i+2])+"\n")
            file.write("\nIRRPROFI   "+str(countdays[i])+". "+str(flux[i])+" "+str(countdays[i+1])+"."+str(flux[i+1])+" "+str(countdays[i+2])+"."+str(flux[i+2]))
        elif i % 2 != 0 and startbeamON == False:
            file.write("\n* Beam ON: " + str(countdays[i]) +" seconds,Beam OFF: "+ str(countdays[i+1])+" seconds,Beam ON: "+str(countdays[i+2])+"\n")
            file.write("\nIRRPROFI   "+str(countdays[i])+". "+str(flux[i])+" "+str(countdays[i+1])+". "+str(flux[i+1])+" "+str(countdays[i+2])+". "+str(flux[i+2]))
       
     
     #for the beginning of lines    
     
    elif i % 3 == 0 and i % 2 == 0 and startbeamON == True:
        # even        
        file.write("\n* Beam ON: " + str(countdays[i]) +" seconds,Beam OFF: "+ str(countdays[i+1]))
        file.write(" seconds,Beam ON: "+str(countdays[i+2]))
        file.write("\nIRRPROFI   "+str(countdays[i])+". "+str(flux[i])+" ")
    
    elif i % 3 == 0 and i % 2 != 0 and startbeamON == True:
        # odd 
        file.write("\n* Beam OFF: " + str(countdays[i]) +" seconds,Beam ON: "+ str(countdays[i+1]))
        file.write(" seconds,Beam OFF: "+str(countdays[i+2]))
        file.write("\nIRRPROFI   "+str(countdays[i])+". "+str(flux[i])+" ")
        
    elif i % 3 == 0 and i % 2 != 0 and startbeamON == False:
        file.write("\n* Beam ON: " + str(countdays[i]) +" seconds,Beam OFF: "+ str(countdays[i+1]))
        file.write(" seconds,Beam ON: "+str(countdays[i+2]))
        file.write("\nIRRPROFI   "+str(countdays[i])+". "+str(flux[i])+" ")
        
    elif i % 3 == 0 and i % 2 == 0 and startbeamON == False:
        file.write("\n* Beam OFF: " + str(countdays[i]) +" seconds,Beam ON: "+ str(countdays[i+1]))
        file.write(" seconds,Beam OFF: "+str(countdays[i+2]))
        file.write("\nIRRPROFI   "+str(countdays[i])+". "+str(flux[i])+" ")
        
        #  middle of lines
    else:
        file.write(" "+str(countdays[i])+". "+str(flux[i])+" ")





