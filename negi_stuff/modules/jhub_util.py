# project name: negi-stuff
# created by diego aliaga daliaga_at_chacaltaya.edu.bo
import re
from pathlib import Path
import os

def get_actual_path(path):
    '''
    returns the actula path of a file from the shareable file
    Parameters
    ----------
    path
        shareable path

    Returns
    -------
    actual path
    '''

    p1 = re.match(
        'https://abisko.uiogeo-apps.sigma2.no/user/(.*)',
        path
    )[1]



    dataporten = '~/shared-ns1000k/dataporten-home/'

    pa = Path(p1)

    user = pa.parts[0]

    rest = pa.parts[3:]

    actual_path = os.path.join(dataporten,user,*rest)

    return actual_path

