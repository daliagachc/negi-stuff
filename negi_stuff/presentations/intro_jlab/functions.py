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

# from imports import *
import matplotlib.pyplot as plt

def custom_plot(x,y):
    '''
    life easier for plotting.
    it will plot x against y 
    '''
    fig, ax = plt.subplots(figsize=(8,4))
    ax.plot(x,y)
    ax.set_title('Example Plot')
    ax.set_ylabel('yyy label')
    ax.set_xlabel('xxxxx label')
    ax.grid()
    return ax

# 