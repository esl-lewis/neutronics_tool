# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 15:13:34 2019
Title: utility functions for irrad tool

"""

import matplotlib.pyplot as plt


def plot_irrad(df):
    """Plots beam current cycle against time."""
    plt.figure()
    x = df.index
    y = df["Average µA"]
    plt.step(x, y)
