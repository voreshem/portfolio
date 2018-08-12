import json
import glob
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.io.img_tiles import GoogleTiles


def parse_strava(source):
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


def gen_sat_map(df):
    '''
    info
    '''

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

            __max__ = max_num + (c*delta)
            __min__ = min_num - (c*delta)

            extent.append(__min__)
            extent.append(__max__)

        extent = list()

        get_extent(min_x, max_x)
        get_extent(min_y, max_y)

        return extent

    ax.set_extent(extent)
    ax.add_image(img, 18)
    x, y = df.lon, df.lat
    ax.plot(x, y, transform=ccrs.Geodetic(), color='orange', linewidth=3)
    plt.savefig("strava_map_" + f.name.strip(".json") + ".png")

def clean_fname(fname):
    '''
    info
    '''
    if fname.endswith('.json') == False and fname.endswith('.JSON') == False:
        return fname + '.json'
    elif fname.endswith('.JSON'):
        return fname.replace('JSON', 'json')
    else:
        return fname


if __name__ == '__main__':
    print('\n'+"The following JSON files are available for mapping:\n")
    [print(filename) for filename in glob.glob("*.json")]

    filename_input = input("Enter JSON filename: \n \n")
    filename_input = clean_fname(filename_input)
    
    good_data = False

    while good_data is False:
        try:
            with open(filename_input) as f:
                source = f.read()
                        
            if True not in [n.startswith(filename_input) for n in glob.glob('*.json')]:
                raise FileNotFoundError
            if 'Strava' not in source:
                raise ValueError

        except FileNotFoundError:
            print('\n'+filename_input + " does not exist...")
            break

        except ValueError:
            print('\n' + f.name + " is not a JSON from Strava!")
            break

        else:
            print("\n" + f.name + " imported successfully!" + (2*"\n") + "Parsing geolocation data!")
            df = parse_strava(source)
            good_data = True

        finally:
            if good_data is True:
                break
            else:
                good_data = False
