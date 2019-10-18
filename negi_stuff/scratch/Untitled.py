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

# %%
from negi_stuff.modules.imps import *

# %%
data_path = '../data_sample/wrf_out.small.h5'

# %%
ds = xr.open_dataset(data_path)

# %%
ds1 = za.change_south_north_west_east_to_lalo(ds)

# %%

# %%
