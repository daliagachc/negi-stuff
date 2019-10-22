import pyaerocom as pya
pya.__version__
pya.const.BASEDIR = '/home/notebook/shared-ns1000k/inputs/pyaerocom-testdata/'
def get_station_coords(station_name, unique=True):
    """
    If match unique, returns tuplet with (<station name>, <lon>, <lat>)
    else prints message and returns Null. 
    Example: Get station coords:
    lon, lat = get_station_coords('Zeppelin')[1:]
    """
    sql_db = pya.io.EbasFileIndex()
    st_coor = sql_db.execute_request('select distinct station_name,station_longitude,station_latitude from station')
    #station_name='Zeppelin'
    match_c = 0
    st_match=[]
    
    for comb in st_coor:
        if unique: test = station_name.strip()==comb[0].strip()
        else: test= station_name in comb[0]
        if test:
            match_c +=1
            print('found station name: %s' %comb[0])
            st_match.append(comb)
    if match_c ==1:
        print('Returning (<station name>, <lon>, <lat>)')
        print(st_match[0])
        return st_match[0]
    else:
        print('Found more than one match, please specify:')
        print(st_match)
    
