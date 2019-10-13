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
def log_example(x):
    if x==1:
        log.ger.error('problem with x %s',x)
    if x==2:
        log.ger.debug('x  is %s',x)
    if x==3:
        log.ger.warning('warning x is %s',x)


# %%
log_example(1)

# %%
log_example(2)

# %%
log_example(3)

# %%
log.ger.setLevel(log.log.DEBUG)

# %%
log_example(1)

# %%
log_example(2)

# %%
log_example(3)

# %%

# %%
log.ger.setLevel(log.log.WARNING)

# %%
log_example(1)

# %%
log_example(2)

# %%
log_example(3)

# %%
