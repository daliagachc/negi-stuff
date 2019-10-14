# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.2.4
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

# %%
#lets define some constants for the variable names so that calling them is easier.
BT  = 'bottom_top'
SN  = 'south_north'
WE  = 'west_east'
time  = 'XTIME'
lat = 'XLAT'
lon = 'XLONG'
P, V, U, T = 'P','V','U','T'

#this is potential temperature in C
T_C = 'T_C'

# %%
# lets process potential temperature into C
ds[T_C] = ds[T] + 300 - 273
ds[T_C] = ds[T_C].assign_attrs({'units': 'C'})

# %% [markdown]
# ## Plotting

# %% [markdown]
# ### Statistics:

# %%
import cartopy.crs as ccrs
fig, axsm = plt.subplots(2,2, figsize=[10,7], subplot_kw={'projection':ccrs.PlateCarree()})
axs = axsm.flatten()
_ds = ds[T_C][{BT:0}]
_ds.mean(time, keep_attrs=True).plot(x=lon, y=lat,ax=axs[0], transform=ccrs.PlateCarree())#, robust=True)
axs[0].set_title('Mean')
_ds.median(time, keep_attrs=True).plot(x=lon, y=lat,ax=axs[1], transform=ccrs.PlateCarree())#, robust=True)
axs[1].set_title('Std')
_ds.quantile(0.05, dim=time, keep_attrs=True).plot(x=lon, y=lat,ax=axs[2], transform=ccrs.PlateCarree())#, robust=True)
_ds.quantile(0.95, dim=time, keep_attrs=True).plot(x=lon, y=lat,ax=axs[3], transform=ccrs.PlateCarree())#, robust=True)
for ax in axs:
    ax.coastlines()
    gl = ax.gridlines()
    ax.add_feature(cy.feature.BORDERS);
plt.tight_layout()

# %%
import cartopy.crs as ccrs
fig, ax = plt.subplots(1, figsize=[10,7], subplot_kw={'projection':ccrs.PlateCarree()})
#axs = axsm.flatten()
WS = 'Wind strength'
ds[WS] = np.sqrt(ds[U]**2+ ds[V]**2)
ds[WS].attrs['units']='m/s'
ds[WS].attrs['name']='Wind strength'

_ds = ds[[U,V, WS]][{BT:0}].mean(XT)
_ds[WS].plot(x=XLO,y=XLA, transform=ccrs.PlateCarree())
ax.quiver(_ds[XLO], _ds[XLA], _ds['U'],_ds['V'], transform=ccrs.PlateCarree())
ax.coastlines()
gl = ax.gridlines()
ax.add_feature(cy.feature.BORDERS);
#plt.tight_layout()

# %% [markdown]
# ### Tired of making plots:

# %%
def sp_map(*nrs, projection = ccrs.PlateCarree(), **kwargs):
    return plt.subplots(*nrs, subplot_kw={'projection':projection}, **kwargs)
    
def add_map_features(ax):
    ax.coastlines()
    gl = ax.gridlines()
    ax.add_feature(cy.feature.BORDERS);



# %%
fig, axs = sp_map(2,3, figsize=[15,8])

T_mm = ds[T][{BT:0}].groupby('XTIME.month').mean(XT)
T_mean = ds[T][{BT:0}].mean(XT)
T_dev = T_mm- T_mean
T_mm.sel(month=1)
for mo, ax in zip(T_mm['month'], axs.flatten()):
    T_dev.sel(month=mo) .plot(ax=ax, transform=ccrs.PlateCarree())
    add_map_features(ax)

