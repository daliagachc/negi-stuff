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
# ## Lets start:
# ### Reading in the data:
# We use xarray here, but you can also use e.g. iris or even pyaerocom

# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

path='../../data_sample/wrf_out.small.h5'
ds = xr.open_dataset(path)

# %% [markdown]
# Check how your dataset looks

# %%
#lets check how the dataset looks like
ds

# %% [markdown]
# Assign attributes! Nice for plotting and to keep track of what is in your dataset (especially 'units' and 'standard_name'/'long_name' will be looked for by xarray.

# %% [markdown]
# **Check the attributes! Can be useful info here:**

# %%
ds['XTIME']

# %%
# lets process potential temperature into C
ds['T_C'] = ds['T'] + 300 - 273
ds['T_C'] = ds['T_C'].assign_attrs({'units': 'C'})

# %% [markdown]
# Easier to type if we define some names:

# %%
#lets define some constants for the variable names so that calling them is easier.
ilev  = 'bottom_top'
SN  = 'south_north'
WE  = 'west_east'
XT  = 'XTIME'
lat = 'XLAT'
lon = 'XLONG'
P, V, U, T = 'P','V','U','T'

#this is potential temperature in C
T_C = 'T_C'

# %% [markdown]
# ## Plotting

# %%
# lets do a basic plot of T_C
ds[T_C][{XT:0, ilev:0}].plot(x=lon, y=lat)

# %%
# lets do a basic plot of P
ds[P][{XT:0, ilev:0}].plot(x=lon, y=lat)

# %%


# lets plot the wind fields
_ds = ds[[V,U]][{ilev:0}]
_ds1 = np.sqrt(_ds[V]**2 + _ds[U]**2)
f,ax = plt.subplots()
_dm = _ds1.mean(XT)
_dm.plot.pcolormesh(cmap = plt.get_cmap('Reds'),ax=ax,cbar_kwargs={'label':'Wind Speed [m/s]'})
ax.set_title('ilev:0; Mean over Time')

# %% [markdown]
# #### Plotting with cartopy

# %%
import cartopy as cy

# %%
f,ax = plt.subplots(subplot_kw={'projection':cy.crs.PlateCarree()})
_ds = ds[[V,U]][{ilev:0}]
_ds1 = np.sqrt(_ds[V]**2 + _ds[U]**2)
_dm = _ds1.mean(XT)
_dm.plot.pcolormesh(
    cmap = plt.get_cmap('Reds'),ax=ax,cbar_kwargs={'label':'Wind Speed [m/s]'},
    transform=cy.crs.PlateCarree(), x=lon,y=lat,
    levels = 6
)
ax.set_title('ilev:0; Mean over Time')
ax.coastlines()

gl = ax.gridlines(draw_labels=True)
gl.xlabels_top = False
gl.ylabels_right = False

ax.add_feature(cy.feature.BORDERS);

# %%
# f,ax = plt.subplots(subplot_kw={'projection':cy.crs.PlateCarree()})
_ds = ds[[V,U]][{ilev:slice(None, None, 2)}]
_ds1 = np.sqrt(_ds[V]**2 + _ds[U]**2)
_dm = _ds1.mean(XT)
p = _dm.plot.pcolormesh(
    cmap = plt.get_cmap('Reds'),cbar_kwargs={'label':'Wind Speed [m/s]'},
    transform=cy.crs.PlateCarree(), x=lon,y=lat,
    levels = 6,
    col=ilev,
    col_wrap = 3,
    subplot_kws={'projection':cy.crs.PlateCarree(),},
    add_colorbar = False,
    size=2,
    aspect = 1.7
)
for ax in p.axes.flatten():
#     ax.set_title('ilev:0; Mean over Time')
    ax.coastlines()

    gl = ax.gridlines(draw_labels=True)
    gl.xlabels_top = False
    gl.ylabels_right = False

    ax.add_feature(cy.feature.BORDERS)
    ax.set_xlim(-90,-40)
    ax.set_ylim(-32,2)
p.fig.canvas.draw()
p.fig.tight_layout()
p.add_colorbar(label='Wind Speed [m/s]');


# %%
