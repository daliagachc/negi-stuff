# project name: psm
# created by diego aliaga daliaga_at_chacaltaya.edu.bo

from bokeh.plotting import figure
from bokeh.io import output_notebook, push_notebook, show

output_notebook()


def figure_dt(*args, **kwargs):
    return figure(*args, **kwargs, x_axis_type='datetime',
                  sizing_mode='stretch_width'   )


figure_dt.__doc__ = figure.__doc__
# plot = figure(x_axis_type='datetime')
# plot.line(y='index',x='time',source=_d1)
# show(plot)
