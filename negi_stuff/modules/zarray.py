# project name: wrf_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo
'''extra functions for xarray'''
import numpy as np
import xarray as xr


def compressed_netcdf_save(
        ds:xr.Dataset,
        path:str,
        shuffle:bool=True,
        complevel:int=4,
        fletcher32:bool=True,
        encode_u:bool=False
):
    '''
    saves the datatase using compression
    Parameters
    ----------
    ds
        input dataset or dataarray
    path
        path to be saved

    shuffle
        improves compression
    complevel
        compression level
    fletcher32
        improves compression?
    encode_u
        sometimes strings produce issues when compressing.
        this takes care of it

    Returns
    -------

    '''
    encoding = {}
    for k, v in ds.variables.items():
        encoding[k] = {
            'zlib'      : True,
            'shuffle'   : shuffle,
            'fletcher32': fletcher32,
            'complevel' : complevel
        }
        if encode_u:
            if v.dtype.kind == 'U':
                encoding[k]['dtype'] = 'S1'
    ds.to_netcdf(path, encoding=encoding)


def cov(xa1, xa2, dim=None):
    """Compute covariance between two DataArray objects along a shared dimension.

    Parameters
    ----------
    xa1: DataArray
        The first array with which the covariance will be computed
    xa2: DataArray
        The other array with which the covariance will be computed
    dim: The dimension along which the covariance will be computed

    Returns
    -------
    covariance: DataArray
    """
    # 1. Broadcast the two arrays
    xa1, xa2 = xr.broadcast(xa1, xa2)

    # 2. Ignore the nans
    valid_values = xa1.notnull() & xa2.notnull()
    xa1 = xa1.where(valid_values, drop=True)
    xa2 = xa2.where(valid_values, drop=True)
    valid_count = valid_values.sum(dim)

    # 3. Compute mean and standard deviation along the given dim
    demeaned_xa1 = xa1 - xa1.mean(dim=dim)
    demeaned_other = xa2 - xa2.mean(dim=dim)

    # 4. Compute  covariance along the given dim
    if dim:
        axis = xa1.get_axis_num(dim=dim)
    else:
        axis = None
    cov = np.sum(demeaned_xa1 * demeaned_other, axis=axis) / (valid_count)

    return cov


def corr(xa1, xa2, dim=None):
    """Compute correlation between two DataArray objects along a shared dimension.

    Parameters
    ----------
    xa1: DataArray
        The first array with which the correlation will be computed
    xa2: DataArray
        The other array with which the correlation will be computed
    dim: The dimension along which the correlation will be computed

    Returns
    -------
    correlation: DataArray
    """
    # 1. Broadcast the two arrays
    xa1, xa2 = xr.broadcast(xa1, xa2)

    # 2. Ignore the nans
    valid_values = xa1.notnull() & xa2.notnull()
    xa1 = xa1.where(valid_values, drop=True)
    xa2 = xa2.where(valid_values, drop=True)

    # 3. Compute correlation based on standard deviations and cov()
    xa1_std = xa1.std(dim=dim)
    other_std = xa2.std(dim=dim)

    return cov(xa1, xa2, dim=dim) / (xa1_std * other_std)


def masked_average(xa, dim=None, weights=None, mask=None):
    """

    :param xa: dataArray
    :param dim: dims
    :param weights: weights (as xarray)
    :param mask: mask (as xarray), True where values to be masked.
    :return:
    """
    xa_ = xa.copy()
    if mask is not None:
        dum, mask_alld = xr.broadcast(xa, mask) # broadcast to all dims
        xa_ = xa_.where(np.logical_not(mask))
        if weights is not None:
            dum, weights_alld = xr.broadcast(xa, weights) # broadcast to all dims
            weights_alld = weights_alld.where(np.logical_not(mask_alld))
            return (xa_*weights_alld).sum(dim=dim)/weights_alld.sum(dim=dim)
        else:
            return xa_.mean(dim)
    elif weights is not None:
        dum, weights_alld = xr.broadcast(xa, weights) # broadcast to all dims
        return (xa_*weights_alld).sum(dim)/weights_alld.where(xa_.notnull()).sum(dim=dim)
    else:
        return xa.mean(dim)


def search_keyword(ds, *keys, print_attrs=True):
    """
    Searches for a keyword in variable names and long_names (if exists) in dataset.
    Returns only variables with all keys.

    :param ds: dataset
    :param keys: keywords
    :return: list of vars that match with keywords
    """
    found_ls = []
    for var in ds.data_vars:
        if 'long_name' in ds[var].attrs:
            all_found=True
            for key in keys:
                if key not in ds[var].attrs['long_name'] and key not in var:
                    all_found=False
            if all_found:
                found_ls.append(var)
                print(var)
                if print_attrs:
                    print(ds[var].attrs)
    return found_ls

def change_south_north_west_east_to_lalo(ds_orig):
    '''
    gets rid of the annoying west_east south_north notation.
    In our case its possible but for other wrf runs this might not be the case
    Parameters
    ----------
    ds

    Returns
    -------
    ds

    '''
    # ds = xr.open_dataset(data_path)
    ds:xr.Dataset = ds_orig
    ds['XLAT' ] = ds['XLAT' ].mean('west_east'  )
    ds['XLONG'] = ds['XLONG'].mean('south_north')
    ds = ds.swap_dims({
        'west_east'  :'XLONG' ,
        'south_north':'XLAT'  ,
    })
    ds = ds.rename_dims({
        'bottom_top' :'ilev'    ,
        'XLAT'       :'lat'     ,
        'XLONG'      :'lon'
    })
    ds = ds.rename_vars({
        'XLAT'       :'lat'     ,
        'XLONG'      :'lon'
    })
    return ds