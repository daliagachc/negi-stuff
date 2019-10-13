import xarray as xr
import numpy as np
import matplotlib.pylab
from matplotlib.colors import LogNorm, SymLogNorm



def groupby_2vars(xa, varList, xedges, yedges, scale='linear'):
    #df = xa.to_dataframe()
    [x,y,z] = varList#[0]
    var = [x,y,z]
    xy = [x,y]
    df1 = xa.to_dataframe().reset_index()[var]
    for ii in np.arange(len(xedges)-1):
        right_x = np.logical_and(df1[x]>xedges[ii], df1[x]<=xedges[ii+1])
        if scale == 'linear': df1[x][right_x] = 0.5*(xedges[ii]+xedges[ii+1])
        elif scale =='log': df1[x][right_x] = 10**(0.5*(np.log10(xedges[ii])+np.log10(xedges[ii+1])))
        df1[x][right_x]=0.5*(xedges[ii]+xedges[ii+1])
    for ii in np.arange(len(yedges)-1):
        right_y = np.logical_and(df1[y] > yedges[ii], df1[y]<=yedges[ii+1])
        if scale == 'linear': df1[y][right_y] = 0.5*(yedges[ii]+yedges[ii+1])
        elif scale =='log': df1[y][right_y] =10**(0.5*(np.log10(yedges[ii])+np.log10(yedges[ii+1])))
    outside = np.logical_or(df1[x] < xedges[0], df1[x]>xedges[-1])
    df1[x][outside] = np.nan
    outside = np.logical_or(df1[y] < yedges[0], df1[y]>yedges[-1])
    df1[y][outside] = np.nan
    nxa = df1.groupby(xy)#.mean().to_xarray()
    return nxa


def plot_cond_statistic( xr_ds, varList, ax, nbins=15, scale = 'linear', stat = 'mean', plt_title = '',
                         quant=0.01, cscale='linear', vmin=999, vmax=-999):
    """
    :param xr_ds: dataset
    :param varList: list of variables [x,y,z]
    :param ax: axis to plot on
    :param nbins: number of bins
    :param scale: 'log' or 'linear'
    :param stat: Now: 'mean' or 'std'
    :param plt_title: Title of subplot
    :param quant: quantile
    :param cscale: scale of colorbar
    :param vmin: come on, you know
    :param vmax: repeat
    :return:
    """

    """

   :return:
    """

    [x, y, z] = varList
    if scale=='linear':
        xedges = np.linspace(xr_ds[x].quantile(quant), xr_ds[x].quantile(1-quant),nbins+1)
        yedges = np.linspace(xr_ds[y].quantile(quant)(), xr_ds[y].quantile(1-quant)(),nbins+1)
    if scale=='log':
        xedges = np.logspace(np.log10(xr_ds[x].compute().quantile(quant).values), np.log10(xr_ds[x].compute().quantile(1-quant).values),num=nbins+1)
        yedges = np.logspace(np.log10(xr_ds[y].compute().quantile(quant).values), np.log10(xr_ds[y].compute().quantile(1-quant).values),num=nbins+1)
    df = groupby_2vars(xr_ds,varList, xedges, yedges, scale=scale)

    if stat=='mean':
        pl_xr = df.mean().to_xarray()[z]#.plot(xscale=scale, yscale=scale, ax=ax, **kwargs)#.to_array().plot()
    if stat=='std':
        pl_xr = df.std().to_xarray()[z]#.plot(xscale=scale, yscale=scale, ax=ax, **kwargs)#.to_array().plot()
    if stat=='count':
        pl_xr = df.count().to_xarray()[z]#.plot(xscale=scale, yscale=scale, ax=ax,**kwargs)#.to_array().plot()
    if vmin==999: vmin= pl_xr.compute().quantile(quant).values#, pl_xr.compute().quantile(1-quant).values
    if vmax==-999: vmax =pl_xr.compute().quantile(1-quant).values
    kwargs= {'vmin':vmin,'vmax':vmax, 'xscale':scale,'yscale':scale}
    if cscale=='log':
        if vmin<=0:
            vmin=vmax*1e-3
            kwargs['vmin']=vmin
            kwargs['norm'] = LogNorm(vmin=vmin, vmax=vmax)
    elif cscale=='symlog': kwargs['norm'] = SymLogNorm(vmin=vmin, vmax=vmax)
    pl_xr.plot(ax=ax,robust = True, **kwargs)
    ax.set_title(plt_title)
    return df, pl_xr