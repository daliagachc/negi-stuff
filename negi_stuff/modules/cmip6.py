# project name: negi-stuff
# created by diego aliaga daliaga_at_chacaltaya.edu.bo

# from negi_stuff.modules.imps import (os, glob, pd)
import os,glob
import pandas as pd
from pathlib import Path

FILES = 'FILE_PATH'
MODEL = 'MODEL'
VAR = 'VAR_NAME'
NAME  = 'filename'
FRQ   = 'FREQUENCY'
RIPF  = 'RIPF'
RR   = 'REALIZATION'
II    = 'INDEX'
PP    = 'PHYSICS'
FF    = 'FORCING'
LABEL = 'LABEL'
ID    = 'ID'
TS    = 'TIME START'
TE    = 'TIME END'
EXP   = 'EXPERIMENT'
from os.path import expanduser

#for better display
pd.options.display.max_colwidth = 1000
def search_cmip6_hist(
        wildcard:str = '*',
        model:str = '*',
        label:str = '*',

) -> pd.DataFrame:
    '''
    searchs the historical cmip6 folder at nird and returns a dataframe
    with the results

    Parameters
    ----------
    wildcard
        pattern for the file name
    model
        pattern or name for the model. default is *
    label
        pattern of name for the label: forcin, index, realization, etc

    Returns
    -------
    df: pd.DataFrame
        dataframe with the results from the search

    Example
    -------
    >>> search_cmip6_hist(wildcard='tas*')

    '''
    home_path = expanduser("~")
    shared_path = 'shared-cmip6-for-ns1000k/historical'


    historical_path = os.path.join(home_path,shared_path,model,label,wildcard)
    files = glob.glob(historical_path)


    #ORDER = [MODEL,NAME,FILES,TS, TE, MON,RIPF,RR,II,PP,FF,LABEL,ID]
    ORDER = [MODEL,NAME,FRQ,FILES,TS, TE, RR,II,PP,FF,LABEL,ID]
    if len(files) is 0:
        return pd.DataFrame([],columns=ORDER)

    df = pd.DataFrame(files,columns=[FILES])

    df[MODEL]   = df[FILES].apply(lambda f: Path(f).parents[1].name)
    df[NAME]    = df[FILES].apply(lambda f: Path(f).name           )
    df[FRQ]     = df[NAME].str.extract('^.*?_[A-Z]*([a-z]*).*_')
    #df[RIPF]  = df[NAME].str.contains('_r.+i.+p.+f.+_')
    #df[VAR]    = df[NAME].str.extract('(\d+)_-\d+.nc')
    df[TS]      = df[NAME].str.extract('_(\d+)-\d+.nc')
    df[TE]      = df[NAME].str.extract('_\d+-(\d+).nc')
    df[RR]      = df[NAME].str.extract('_r(.+?)i.+p.+f.+_').astype(int)
    df[II ]     = df[NAME].str.extract('_r.+i(.+?)p.+f.+_').astype(int)
    df[PP ]     = df[NAME].str.extract('_r.+i.+p(.+?)f.+_').astype(int)
    df[FF ]     = df[NAME].str.extract('_r.+i.+p.+f(.+?)_').astype(int)
    df[LABEL ]  = df[NAME].str.extract('_(r.+i.+p.+f.+?)_')
    df[ID]      = df[MODEL]+df[LABEL]

    df = df[ORDER]
    return df

# project name: negi-stuff
# created by diego aliaga daliaga_at_chacaltaya.edu.bo

# from negi_stuff.modules.imps import (os, glob, pd)

from os.path import expanduser
def search_cmip6(
        wildcard  :str = '*',
        model     :str = '*',
        label     :str = '*',
        experiment:str = '*',

) -> pd.DataFrame:
    '''
    searchs the cmip6 folder at nird and returns a dataframe
    with the results

    Parameters
    ----------
    wildcard
        pattern for the file name
    model
        pattern or name for the model. default is *
    label
        pattern of name for the label: forcin, index, realization, etc
    experiment
        pattern of the experiment e.g historical

    Returns
    -------
    df: pd.DataFrame
        dataframe with the results from the search

    Example
    -------
    >>> search_cmip6_hist(wildcard='tas*')

    '''
    home_path = expanduser("~")
    shared_path = 'shared-cmip6-for-ns1000k'


    historical_path = os.path.join(home_path,
                                   shared_path,
                                   experiment,
                                   model,
                                   label,
                                   wildcard)
    #     print(historical_path)
    files = glob.glob(historical_path)


    #ORDER = [MODEL,NAME,FILES,TS, TE, MON,RIPF,RR,II,PP,FF,LABEL,ID]
    ORDER = [MODEL,NAME,EXP,FRQ,FILES,TS, TE, RR,II,PP,FF,LABEL,ID]
    #     return files
    if len(files) is 0:
        return pd.DataFrame([],columns=ORDER)

    df = pd.DataFrame(files,columns=[FILES])
    df[EXP]     = df[FILES].apply(lambda f: Path(f).parents[2].name)
    df = df[~(df[EXP]=='scripts')]
    df = df[~(df[EXP]=='raw'    )]
    df[MODEL]   = df[FILES].apply(lambda f: Path(f).parents[1].name)
    df[NAME]    = df[FILES].apply(lambda f: Path(f).name           )
    df[FRQ]     = df[NAME].str.extract('^.*?_[A-Z]*([a-z]*).*_')
    #df[RIPF]  = df[NAME].str.contains('_r.+i.+p.+f.+_')
    #df[VAR]    = df[NAME].str.extract('(\d+)_-\d+.nc')
    df[LABEL ]  = df[NAME].str.extract('_(r.+i.+p.+f.+?)_')
    df = df[~df[LABEL].isna()]
    df[TS]      = df[NAME].str.extract('_(\d+)-\d+.nc')
    df[TE]      = df[NAME].str.extract('_\d+-(\d+).nc')
    df[RR]      = df[NAME].str.extract('_r(.+?)i.+p.+f.+_').astype(int)
    df[II ]     = df[NAME].str.extract('_r.+i(.+?)p.+f.+_').astype(int)
    df[PP ]     = df[NAME].str.extract('_r.+i.+p(.+?)f.+_').astype(int)
    df[FF ]     = df[NAME].str.extract('_r.+i.+p.+f(.+?)_').astype(int)
    df[ID]      = df[MODEL]+df[LABEL]

    df = df[ORDER]
    return df