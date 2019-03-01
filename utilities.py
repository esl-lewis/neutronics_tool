# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 15:13:34 2019
Title: utility functions for irrad tool

"""

import matplotlib.pyplot as plt
import logging
from format_from_EXCEL import formatExcel


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
