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
# # Introduction 2:
# ## Visualization in jupyter notebook
#
#
# ### Reading in the data:
# - We use xarray here, but you can also use e.g. iris or even pyaerocom!
# - We recomend however, that you use a package that keeps track of your coordinates in your data and the metadata in your data! (E.g. numpy doesn't do this) 
# - This is also why the NetCDF format is so popular -- it keeps track of these things and is extremely easy to load with these packages. 
#

# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
# or
# from imports import (plt, np, xr)
path='../../data_sample/wrf_out.small.h5' 
ds = xr.open_dataset(path)#, decode_times=False)

# %% [markdown]
# Check how your dataset looks

# %%
#lets check how the dataset looks like
ds

# %% [markdown]
# **Check the attributes! Can be useful info here:**

# %%
ds['XTIME']

# %% [markdown]
# **Assign attributes!** Nice for plotting and to keep track of what is in your dataset (especially 'units' and 'standard_name'/'long_name' will be looked for by xarray.

# %%
# lets process potential temperature into C
ds['T_C'] = ds['T'] + 300 - 273
ds['T_C'] = ds['T_C'].assign_attrs({'units': 'C'})

# %%
# lets do a basic plot of T_C
ds['T_C'].isel(XTIME=0,bottom_top=0).plot()
# analogy:
#ds[T_C][{ilev:0,time:0}].plot()

# %% [markdown]
# The coordinate 'south_north' annoyes me, so I change it!

# %%
# Initially just a number, I want the actual latitude!
ds['south_north'] = ds.XLAT[:,0]
ds['west_east']   = ds.XLONG[0,:]
# Rename them!
ds=ds.rename({'south_north':'lat',
              'west_east'  :'lon'    })

# %%
## from zarray import : 

# %% [markdown]
# Easier to type if we define some names:

# %%
#lets define some constants for the variable names so that calling them is easier.
ilev = 'bottom_top'
lat = 'lat'
lon = 'lon'
XT  = 'XTIME'
time = 'XTIME'
lat = 'XLAT'
lon = 'XLONG'
P, V, U, T = 'P','V','U','T'

#this is potential temperature in C
T_C = 'T_C'

# %% [markdown]
# ## Plotting

# %%
# lets do a basic plot of T_C
ds[T_C].isel(XTIME=0,bottom_top=0).plot()

# analogy:
#ds[T_C][{ilev:0,time:0}].plot()

# %% [markdown]
# ### Make new variables:

# %%
WS = 'Wind speed'

ds[WS] = np.sqrt(ds[U]**2+ ds[V]**2)

ds[WS].attrs['units']='m/s'
ds[WS].attrs['name']='Wind speed'

# %% [markdown]
# ## Use cartopy

# %%
import cartopy as cy

# %%
f,ax = plt.subplots(subplot_kw={'projection':cy.crs.PlateCarree()})
_ds = ds[{ilev:0}]
_dm = _ds[WS].mean(time, keep_attrs=True)
_dm.plot.pcolormesh(
    cmap     = plt.get_cmap('Reds'),
    ax       = ax,
    transform= cy.crs.PlateCarree(),
    levels   = 6
)

ax.set_title('BT:0; Mean over Time')
ax.coastlines()

gl = ax.gridlines(draw_labels=True)
gl.xlabels_top   = False
gl.ylabels_right = False
ax.add_feature(cy.feature.BORDERS);

# %% [markdown]
# ### Quick statistics:

# %%
import cartopy.crs as ccrs
import cartopy as cy
fig, axsm = plt.subplots(2,2, 
                         figsize=[10,7], 
                         subplot_kw={'projection':ccrs.PlateCarree()})
axs = axsm.flatten()
_ds = ds[T_C][{ilev:0}]
_ds.mean(time, keep_attrs=True).plot(ax=axs[0], 
                                     transform=ccrs.PlateCarree(), 
                                     robust=True)
axs[0].set_title('Mean')
_ds.std(time, keep_attrs=True).plot(ax=axs[1], 
                                    transform=ccrs.PlateCarree())#, robust=True)
axs[1].set_title('Std')
_ds.quantile(0.05, dim=time, keep_attrs=True).plot(ax=axs[2], 
                                                   transform=ccrs.PlateCarree())#, robust=True)
_ds.quantile(0.95, dim=time, keep_attrs=True).plot(ax=axs[3], 
                                                   transform=ccrs.PlateCarree())#, robust=True)
for ax in axs:
    ax.coastlines()
    gl = ax.gridlines()
    ax.add_feature(cy.feature.BORDERS);
    gl.xlabels_top = False
    gl.ylabels_right = False

plt.tight_layout()

# %%
import cartopy.crs as ccrs
import cartopy as cy
fig, ax = plt.subplots(1, 
                       figsize=[10,7], 
                       subplot_kw={'projection':ccrs.PlateCarree()})

_ds = ds[[U,V, WS]][{ilev:0}].mean(XT) #keep_attrs=True)
_ds[WS].plot(x=lon, y=lat, transform=ccrs.PlateCarree())
ax.quiver(_ds[lon], 
          _ds[lat], 
          _ds['U'],
          _ds['V'], 
          transform=ccrs.PlateCarree())
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
    gl = ax.gridlines(draw_labels=True)
    gl.xlabels_top = False
    gl.ylabels_right = False




# %%
fig, axs = sp_map(2,3, figsize=[18,8], sharex=True, sharey=True)

# Use groupby! (doesn't need to be in time):
T_mm = ds[T][{ilev:0}].groupby('XTIME.month').mean(XT)
T_mean = ds[T][{ilev:0}].mean(XT)
# let's check the deviation from the mean over the whole period! (Easier to see)

# MARK: THIS WOULD NOT WORK IN NUMPY!
T_dev = T_mm- T_mean
for mo, ax in zip(T_mm['month'], axs.flatten()):
    T_dev.sel(month=mo).plot(x=lon, y=lat, ax=ax, transform=ccrs.PlateCarree())
    add_map_features(ax)
plt.tight_layout()


# %%
fig, axs = sp_map(2,3, figsize=[18,8])
# select bottom layer and group by month and apply mean:
W_mm = ds[{ilev:0}].groupby('XTIME.month').mean(XT)

for mo, ax in zip(T_mm['month'], axs.flatten()):
    _dsm = W_mm.sel(month=mo)
    _dsm[WS].plot(x=lon, y=lat, ax=ax, transform=ccrs.PlateCarree())
    ax.quiver(_dsm[lon], _dsm[lat], 
              _dsm['U'], _dsm['V'], 
              transform=ccrs.PlateCarree(), color='w')

    add_map_features(ax)
plt.tight_layout()


# %% [markdown]
# ## Lev lat plot:

# %%
ds[U].mean([time, 'lon']).plot.contourf(robust=True)

# %% [markdown]
# ## Typical pandas methods often apply (or have an analogy): Daily max, daily min.
# Google xarray and the name of your favorite function

# %%
ds_dmax = ds.resample(XTIME='1D').max()
ds_dmin = ds.resample(XTIME='1D').min()


# %%
ds_dmax

# %%
fig, ax = sp_map(1, figsize = [8,5])
ds_diffmm = ds_dmax -ds_dmin
_diff = ds_diffmm[{ilev:0}].mean(time)
kwargs = { 'transform':ccrs.PlateCarree()}
_diff[T_C].plot(x=lon, y=lat, ax=ax, **kwargs)
ax.set_title(r'$\theta$: Mean daily difference max- min')
add_map_features(ax)
plt.tight_layout()

# %% [markdown]
# ## Check a particular place (e.g. to compare to observations)
# Chacaltaya measuring station is located at roughly (-16.34, -68.12). We will pick out the grid cell closest to this. 

# %%
CHC =      {'lat' : -16.34, 'lon' : -68.12}
#marine =   {'lat' : -16.44, 'lon' : -72.24}
#amazonas = {'lat' : -5.08,  'lon' : -64.44}

# %%
ds

# %%
_ds = ds[{ilev:0}]
ds_chc = _ds.sel(lat=CHC['lat'], 
                 lon=CHC['lon'],
                 method='nearest')

# %%
ax = plt.axes(projection=cy.crs.PlateCarree())
ax.set_extent([ds[lon].min(),
               ds[lon].max(),
               ds[lat].min(),
               ds[lat].max()
              ])
ax.scatter(ds_chc[lon],ds_chc[lat])
ax.coastlines()
ax.add_feature(cy.feature.BORDERS);
gl = ax.gridlines(draw_labels=True,color='k',alpha=.1)

# %%
_df = ds_chc.to_dataframe()

# %%
f, ax = plt.subplots()
_group = _df['T'].groupby(_df.index.hour)
qs = [.25,.5,.75]
for q in qs:
    _group.quantile(q).plot(ax=ax, label=q)

# %%
ax.set_title(ds['T'].description)
ax.legend(title='quantiles')
ax.figure

# %% [markdown]
# #### More plotting with pandas:
# - https://pandas.pydata.org/pandas-docs/stable/user_guide/visualization.html
#

# %%
import seaborn as sns
sns.distplot(_df['T'])
