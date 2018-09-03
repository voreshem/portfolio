import json
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.io.img_tiles import GoogleTiles
from sklearn.cluster import KMeans

def gen_sat_map(df, place=False):
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
    
    if place == True:
        locs = df.values

        kmeans = KMeans(n_clusters=10)
        kmeans.fit(locs)

        buoys = kmeans.cluster_centers_
        r_buoys = buoys.round(6)
        
        df = pd.DataFrame(columns=['lon', 'lat'], data=r_buoys)

        x, y = df.lon, df.lat
        ax.plot(x, y, 'ro', markersize=35, transform=ccrs.Geodetic());
        plt.savefig(f.name.strip(".json") + "_sites" + ".png", bbox_inches='tight')

        print("\nSaving buoy coordinates to text file!")
        F = open("buoy_placement_coordinates.txt", 'w')
        F.write("Buoy Placement Coordinates: \n")
        for x,y in r_buoys:
            loc = '\n\n' + str(y) + ', ' + str(x)
            F.write(loc)
        F.close()


    else:
        x, y = df.lon, df.lat
        ax.plot(x, y, transform=ccrs.Geodetic(), color='red', linewidth=5);
        plt.savefig(f.name.strip(".json") + ".png", bbox_inches='tight')



with open('buoy_placement.json') as f:
    source = f.read()

sdic = json.loads(source)

fdic = sdic['features'][0]

gdic = fdic['geometry']

locdat = gdic['coordinates']

lonlat = [n[:2] for n in locdat]

df = pd.DataFrame(columns=['lon', 'lat'], data=lonlat)

gen_sat_map(df)
gen_sat_map(df, place=True)

print("\nDONE")
