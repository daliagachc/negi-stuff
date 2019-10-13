# project name: wrf_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo
'''extra functions for xarray'''
import numpy as np
import xarray as xr


def compressed_netcdf_save(ds, path, shuffle=True, complevel=4, fletcher32=True, encode_u=False):
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