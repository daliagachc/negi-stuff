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

from imports import *

def custom_plot(x,y):
    fig, ax = plt.subplots(figsize=(6,4))
    ax.plot(x,y)
    ax.set_title('Example Plot')
    ax.set_ylabel('y label')
    ax.set_xlabel('x label')
    ax.grid()
    return ax

# a