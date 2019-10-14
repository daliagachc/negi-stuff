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

# %% [markdown]
#

# %% [markdown]
#

# %% [markdown]
# ## Functions
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

# %% {"jupyter": {"outputs_hidden": true}}
np.array([1,2])

# %% {"jupyter": {"outputs_hidden": true}}
plt.plot([1],[1])

# %%
from negi_stuff.modules.imps import (
        pd, np, xr, za, mpl, plt, sns, pjoin, os,
        glob, dt, sys, ucp, log, crt
    )

# %% [markdown]
# or if you want to be more intuitive although not recommended by convention

# %%
from negi_stuff.modules.imps import *

# %% {"jupyter": {"outputs_hidden": true}}
?? negi_stuff.modules.imps

# %% [markdown]
# ## Scripts

# %%
link to [script](04-interaction.py)

# %% [markdown]
# ## Packages

# %% [markdown]
#

# %% [markdown]
#

# %% [markdown]
#
