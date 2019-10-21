# project name: negi-stuff
# created by diego aliaga daliaga_at_chacaltaya.edu.bo
'''
extra functionality for pandas
Examples
-----
>>> from negi_stuff.modules import koalas as kl
'''

import numpy as np
import cftime
import pandas as pd

def check_transform_cftime_dim_2_timestamp(
        df:pd.DataFrame,
        # time_name = 'time',
        middle_of_month = False
) -> pd.DataFrame:
    '''
    fixes problems with cftime objects not being converted into timestamp
    objects by xarray.
    it assumes that the frequency of your dataset is lower or equal to months.
    Otherwise, this conversion might not be right.
    it assumes time column is the index already
    Parameters
    ----------
    df
        input
    middle_of_month
        if cftime.Datetime360Day then values like (2019,2,30) are allowed
        but that makes no sense in pd.Timestamp so we set it to 15 days to
        be in the middle and avoid the error

    Returns
    -------
    df with the modified time so that its a pd.Timestamp object

    '''

    time_first_element = df.index.values[0]

    time_type = type(time_first_element)



    is_type_cftime = (
            (time_type == cftime._cftime.DatetimeNoLeap) | \
            (time_type == cftime._cftime.Datetime360Day)
    )

    if is_type_cftime:
        # transform to pd.timestamp object
        orig_name = df.index.name
        if orig_name == None:
            orig_name = 'time'
            df.index.name = orig_name

    time_xr_index = df.to_xarray()[orig_name]
    # time_dim_string = time_xr_index.dt.strftime(time_first_element.format)
    #     df.index = pd.to_datetime(time_dim_string)
    y = 'Year'
    m = 'Month'
    d = 'Day'
    tc = [m,d,y]
    time_xr_index[y] = time_xr_index.dt.year
    time_xr_index[m] = time_xr_index.dt.month
    time_xr_index[d] = time_xr_index.dt.day
    if middle_of_month:
        time_xr_index[d] = 15
    _df = time_xr_index.to_dataframe().drop('time',axis=1).reset_index()
    _df['time'] = pd.to_datetime(_df[tc])
    df.index = _df['time']

    return df