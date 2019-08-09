# neutronics_tool

This tool plots the beam current of a neutron spallation. It takes an excel spreadsheet as input and converts the data into formats fit for the FISPACT, CINDER and FLUKA simulation packages.
It allows a user to select dates between which to plot a graph of the accelerator beam cycle behaviour over time. 

Initial processing, date selectivity and graph plotting is performed in format_from_EXCEL. Each of the following components writes an input file compliant with the formatting requirements for three simulation codes which can be fairly strict. 

The goal is to enable a neutronics scientist to examine a timespan of interest and rapidly create an input file for further analysis with a modelling code. 

## requirements
Need to have your own excel file with appropriate multiple columns for start date, end date and average beam current - not included in the repo
Need to have pandas version 0.23 or greater and xlrd. 

