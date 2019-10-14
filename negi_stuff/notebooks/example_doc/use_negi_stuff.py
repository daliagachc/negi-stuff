# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.2.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Use negi_stuff

# %% [markdown]
# ### If not installed in your conda environment:
# Add path to folder to the python path:

# %%
import sys
sys.path.append('../../')

# %% [markdown]
# ### continue

# %%

# %%
from negi_stuff.modules.imps import (pd,np,xr,za,mpl,plt,sns, pjoin, os,glob,dt,
    sys,ucp,log, splot, crt)

# %% [markdown]
# You have now enabled autoreload (which will automatically reload a module if it has changed since load), and imported pandas as pd, numpy as np, xarray as xr, matplotlib as mpl, matplotlib.pyplot as plt, seaborn as sns, etc etc (check file for rest)

# %%
ucp.set_dpi(100)

# %%
from negi_stuff.modules.plot.plot import calc_vmin_vmax
list_xr = []
for i in range(5):
    data = np.random.rand(4, 5)
    locs = np.arange(5)
    times = pd.date_range('2000-01-01', periods=4)
    foo = xr.DataArray(data, coords=[times, locs], dims=['time', 'space'])
    list_xr.append(foo)
###################
# calc vmin and vmax in all plots
vmin, vmax = calc_vmin_vmax(list_xr)
###################
fig, axs = plt.subplots(5,figsize=(5,10),sharex=True)
for ax, da in zip(axs, list_xr):
        da.plot(ax=ax, vmin=vmin, vmax=vmax)

# %%
