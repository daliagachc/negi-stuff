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
XT  = 'XTIME'
XLA = 'XLAT'
XLO = 'XLONG'
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
import cartopy as cy
fig, axsm = plt.subplots(2,2, figsize=[10,7], subplot_kw={'projection':ccrs.PlateCarree()})
axs = axsm.flatten()
_ds = ds[T_C][{BT:0}]
_ds.mean(time, keep_attrs=True).plot(x=lon, y=lat,ax=axs[0], transform=ccrs.PlateCarree(), robust=True)
axs[0].set_title('Mean')
_ds.std(time, keep_attrs=True).plot(x=lon, y=lat,ax=axs[1], transform=ccrs.PlateCarree())#, robust=True)
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
import cartopy as cy
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
fig, axs = sp_map(2,3, figsize=[18,8])

T_mm = ds[T][{BT:0}].groupby('XTIME.month').mean(XT)
T_mean = ds[T][{BT:0}].mean(XT)
T_dev = T_mm- T_mean
T_mm.sel(month=1)
for mo, ax in zip(T_mm['month'], axs.flatten()):
    T_dev.sel(month=mo).plot(x=XLO, y=XLA,ax=ax, transform=ccrs.PlateCarree())
    add_map_features(ax)
plt.tight_layout()


# %%
fig, axs = sp_map(2,3, figsize=[18,8])

W_mm = ds[{BT:0}].groupby('XTIME.month').mean(XT)
#W_mean = ds[T][{BT:0}].mean(XT)
#T_dev = T_mm- T_mean
#T_mm.sel(month=1)
for mo, ax in zip(T_mm['month'], axs.flatten()):
    _dsm = W_mm.sel(month=mo)
    _dsm[WS].plot(x=XLO, y=XLA,ax=ax, transform=ccrs.PlateCarree())
    ax.quiver(_dsm[XLO], _dsm[XLA], _dsm['U'],_dsm['V'], transform=ccrs.PlateCarree(), color='w')
    
    add_map_features(ax)
plt.tight_layout()


# %%
_ds = ds.copy()
_ds['south_north'] = ds[XLA][:,0]
_ds = _ds.rename({'south_north':'lat'})
_ds[U].mean([XT,'west_east']).plot.contourf(robust=True)

# %%
ds_dmax = ds.groupby('XTIME.day').max()
ds_dmin = ds.groupby('XTIME.day').min()

# %%
ds_dmax

# %%
fig, axsm =sp_map(2,2, figsize = [12,7])
axs = axsm.flatten()
_max = ds_dmax[{BT:0}].mean('day')
_min = ds_dmin[{BT:0}].mean('day')
kwargs = { 'transform':ccrs.PlateCarree()}
_max[T_C].plot(x=XLO, y=XLA, ax=axs[0],**kwargs )
_min[T_C].plot(x=XLO, y=XLA,ax=axs[1],**kwargs )
axs[0].set_title('T max')
axs[1].set_title('T min')
_max[WS].plot(x=XLO, y=XLA,ax=axs[2],**kwargs )
_min[WS].plot(x=XLO, y=XLA,ax=axs[3],**kwargs )
axs[2].set_title('Wind max')
axs[3].set_title('Wind min')
for ax in axs:
    add_map_features(ax)
plt.tight_layout()

# %%
CHC ={'XLAT':-16.20, 'XLONG':-40.6} 
marine = {'XLAT':-16.44, 'XLONG': -72.24}
amazonas = {'XLAT':-5.08, 'XLONG':-64.44}#'29.4"W

# %%
locations={'CHC':CHC, 'marine':marine, 'amazonas':amazonas}

# %%
locations = ['marine', 'CHC','amazonas']
ds2 = ds.copy()
ds2['south_north'] = ds2.XLAT[:,0]
ds2['west_east']=ds2.XLONG[0,:]
ds2=ds2.rename({'south_north':'lat','west_east':'lon'})

# %%
li=[]
for loc in locations:
    li.append(ds2.sel(lat=locations[loc]['XLAT'], lon=locations[loc]['XLONG'] , method='nearest'))

ds_loc= xr.concat(li, dim='location')#{'LOC':list(locations.keys())})
ds_loc['location']=list(locations.keys())
ds_loc

# %%
fig, axs = plt.subplots(2,1, sharex=True)
for loc in ds_loc.location.values:
    ds_loc[{BT:0}]['Wind strength'].sel(location=loc).plot(label=loc,ax=axs[0])
    axs[0].set_title('All values')
    ds_loc[{BT:0}]['Wind strength'].sel(location=loc).rolling(XTIME=8).mean().plot(label=loc,ax=axs[1])
    axs[1].set_title('Rolling 24 h mean')
    
axs[1].legend()
plt.tight_layout()

# %% [markdown]
# ## Convert to pandas:

# %%
df_loc = ds_loc[{BT:0}].to_dataframe()

# %%
df_loc
