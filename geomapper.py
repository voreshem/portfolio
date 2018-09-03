import json
import xmltodict
import glob
import os
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.io.img_tiles import GoogleTiles


def parse_json(source):
    '''
    info
    '''

    strava_dict = json.loads(source)
    strava_data = strava_dict['data'][0]

    strava_data['fields'].insert(1, 'lat')
    strava_data['fields'].insert(2, 'lon')
    strava_data['fields'].remove('latlng')

    for value in strava_data['values']:
        latlng = value[1]
        value[1:1] = [n for n in latlng]
        value.remove(latlng)

    df = pd.DataFrame(columns=strava_data['fields'], data=strava_data['values'])
    return df

def parse_gpx(source):
    '''
    info
    '''
    strava_data = xmltodict.parse(source)
    strava_data = strava_data['gpx']['trk']['trkseg']['trkpt']
    df = pd.DataFrame(strava_data)
    df.columns = ['lat', 'lon', 'ele', 'time']
    df = df[['lat', 'lon']].apply(pd.to_numeric)
    return df


def gen_sat_map(df):
    '''
    info
    '''
    print("\nDownloading data and plotting map!")

    img = GoogleTiles(
        url='https://server.arcgisonline.com/ArcGIS/rest/services'
        '/World_Imagery/MapServer/tile/{z}/{y}/{x}.jpg')
    plt.figure(figsize=(100, 100))
    ax = plt.axes(projection=img.crs)

    def gen_map_extent(df):
        '''
        info
        '''
        c = 0.05

        min_x, max_x = min(df.lon), max(df.lon)
        min_y, max_y = min(df.lat), max(df.lat)

        def get_extent(min_num, max_num):
            '''
            info
            '''
            diff = max_num - min_num
            delta = (diff/min_num)*100

            if max_num > 0 and min_num > 0:
                __max__ = max_num + (c*delta)
                __min__ = min_num - (c*delta)

            elif max_num < 0 and min_num < 0:
                __max__ = max_num - (c*delta)
                __min__ = min_num + (c*delta)

            extent.append(__min__)
            extent.append(__max__)

        extent = list()

        get_extent(min_x, max_x)
        get_extent(min_y, max_y)

        return extent

    extent = gen_map_extent(df)

    ax.set_extent(extent)
    ax.add_image(img, 18)
    x, y = df.lon, df.lat
    ax.plot(x, y, transform=ccrs.Geodetic(), color='purple', linewidth=5);
    plt.savefig("./maps/strava_map_" + f.name.strip(f.name[-4:]) + ".png", bbox_inches="tight")
    plt.close()

def clean_fname(fname):
    '''
    info
    '''
    if fname in filelist:
        return [file for file in filelist if fname in file][0]

    elif any([file.startswith(fname) for file in filelist]) == True:
        return [file for file in filelist if file.startswith(fname)][0]

    else:
        return fname

def auto(source):
    '''
    info
    '''
    if 'gpx' in source:
        df = parse_gpx(source)
        gen_sat_map(df)

    elif 'json' in source:
        df = parse_json(source)
        gen_sat_map(df)


if __name__ == '__main__':
    filelist = (glob.glob("*.json") + glob.glob("*.gpx"))
    print("\nThe following JSON & GPX files are available for mapping:\n")
    [print(filename) for filename in filelist]

    filename_input = input("Enter JSON or GPX filename: \n \n")
    filename_input = clean_fname(filename_input)
    
    good_data = False

    while good_data is False:
        try:
            with open(filename_input) as f:
                source = f.read()
                        
            if True not in [n.startswith(filename_input) for n in filelist]:
                raise FileNotFoundError
            if 'Strava' not in source:
                raise ValueError

        except FileNotFoundError:
            print('\n'+filename_input + " does not exist...")
            break

        except ValueError:
            print('\n' + f.name + " is not a JSON or GPX from Strava!")
            break

        else:
            print("\n" + f.name + " imported successfully!" + (2*"\n") + "Parsing geolocation data!")
            
            if f.name.endswith('.gpx') == True:
                df = parse_gpx(source)
                good_data = True

            elif f.name.endswith('.json') == True:
                df = parse_json(source)
                good_data = True

        finally:
            if good_data is True:
                break
            else:
                good_data = False

    gen_sat_map(df)
    print("DONE!")

else:
    filelist = (glob.glob("*.json") + glob.glob("*.gpx"))
    numfiles = len(filelist)
    print("\nPlotting all " + str(numfiles) + " JSON & GPX files in current directory!\n")
    if not os.path.exists('maps'):
        os.makedirs('maps')
    for fname in filelist:
        print("\nProcessing file: " + str(filelist.index(fname)+1) + '/' + str(numfiles) + '...\n')
        with open(fname) as f:
            source = f.read()
        auto(source)
        print("\nFile DONE!")
    print("\nFINISHED!")
