# project name: useful-scit
# created by diego aliaga daliaga_at_chacaltaya.edu.bo
"""
useful imports for exploratory analysis should be used as:
Examples:
better to do
    from negi_stuff.modules.imps import (
        pd, np, xr, za, mpl, plt, sns, pjoin, os,
        glob, dt, sys, ucp, log, crt
    )

DEPRECATED (not recommended by convention)
    from from negi_stuff.modules.imps import *

so that all short names are in the name space
be careful not to add any def that could shadow other definitions
"""

# %% imports


import pandas as pd
import numpy as np
import xarray as xr
import negi_stuff.modules.zarray as za
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import importlib as il
import os
import glob
import datetime as dt
import sys
import cartopy as crt

# list of thing to make ploting life easier.
import negi_stuff.modules.plot.plot as ucp

# so that logging is out of the box
import negi_stuff.modules.log as log


# %% reload


def load_and_reload():
    '''
    the code below automatically reload modules that
    have being changed when you run any cell.
    If you want to call in directly from a notebook you
    can use:
    Example
    ---
    >>> %load_ext autoreload
    >>> %autoreload 2
    '''
    from IPython import get_ipython

    try:
        _ipython = get_ipython()
        _ipython.magic('load_ext autoreload')
        _ipython.magic('autoreload 2')
    except:
        # in case we are running a script
        pass


load_and_reload()

# %% shortcuts
pjoin = os.path.join

splot = plt.subplots

# %%


# for plotting stuff
# from IPython.display import set_matplotlib_formats

# set_matplotlib_formats('png')


# plt.style.use('ggplot')

# bokeh

import negi_stuff.modules.plot.bokeh as bok

# useful shortcuts
