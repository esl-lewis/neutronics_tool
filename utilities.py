# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 15:13:34 2019
Title: utility functions for irrad tool

"""
from math import log10, floor
import matplotlib.pyplot as plt
import logging
import datetime
from format_from_EXCEL import formatExcel


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


def currentTOflux(I):
    """ Converts beam current (µA) into flux
    """
    I = I/1e6  # conversion from microamps to amps
    qp = 1.6e-19  # charge of proton in Coulombs
    flux = I / (qp)
    return flux


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

def format_E(variable, number_sigfig):
    if variable == 0:
        return '0.0'
    elif number_sigfig == 1:
        return'{:.1E}'.format(variable)
    elif number_sigfig == 2:
        return'{:.2e}'.format(variable)
# note upper and lowercase E/e is on purpose, depends on CINDER/FLUKA preferred input
