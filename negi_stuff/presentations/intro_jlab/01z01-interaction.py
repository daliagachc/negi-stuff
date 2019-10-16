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
# ## Exploratory Data Analysis
# - Exploratory Data Analysis in Jupyter Lab
#     - Positive
#         - Fast
#         - Prototype
#         - Instant Feedback
#     - Negative
#         - Notebooks can become unmanagable
#         - Tendency to do repetitive tasks
#         - hard to reuse

# %% [markdown]
# ## Imports

# %% [markdown]
# link to [imps](../../modules/imps.py) 

# %%
np.array([1,2])

# %%
plt.plot([1],[1])

# %%
from imports import (
        pd, np, xr, za, mpl, plt, sns, os,
        glob, dt, sys, crt
    )

# %% [markdown]
# or if you want to be more intuitive although not recommended by convention

# %%
from imports import *

# %%

# %%

# %% [markdown]
# link to [imps](./imports.py) 

# %%
np.array([1,2])

# %%
plt.plot([1,2],[1,2])

# %% [markdown]
# ## Scripts and Functions

# %% [markdown]
# link to 
# [script](04-interaction.py)
# (python) version of this notebook
# (you need jupytext extension for it to work)

# %%
x = [1,2,3,4,5]
y = [1,2,3,2,1]
fig, ax = plt.subplots(figsize=(6,4))
ax.plot(x,y)
ax.set_title('Example Plot')
ax.set_ylabel('y label')
ax.set_xlabel('x label')
ax.grid()


# %% [markdown]
# lets write a function for the code above

# %%
def custom_plot(x,y):
    fig, ax = plt.subplots(figsize=(6,4))
    ax.plot(x,y)
    ax.set_title('Example Plot')
    ax.set_ylabel('y label')
    ax.set_xlabel('x label')
    ax.grid()
    return ax


# %%
ax = custom_plot([1,2,3],[3,2,1])

# %% [markdown]
# lets put the function in the functions.py file

# %%
import functions as fu

# %%
ax = fu.custom_plot([1,2,3],[3,2,1])

# %%
# %load_ext autoreload
# %autoreload 2

# %%

# %%
ax = fu.custom_plot([1,2,3],[3,2,1])

# %%
ax = fu.custom_plot([1,2,3],[3,2,1])

# %% [markdown]
# ok, so now we are ready to start a 
# [notebook](./exploratory_data_analysis.ipynb)
#

# %%


# %% [markdown]
#

# %% [markdown]
#

# %% [markdown]
#
