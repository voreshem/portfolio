#!/usr/bin/env python3

####----*----buoy_placement----*----####
"""
buoy_placement takes a
"""

import xmltodict
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.io.img_tiles import GoogleTiles
from geopy.distance import geodesic as gdis
from sklearn.cluster import KMeans


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

        df = pd.DataFrame(columns=['lat', 'lon'], data=r_buoys)

        x, y = df.lon, df.lat
        ax.plot(x, y, 'ro', markersize=35, transform=ccrs.Geodetic());
        plt.savefig(f.name.strip(".gpx") + "_sites" + ".png", bbox_inches='tight')

    else:
        x, y = df.lon, df.lat
        ax.plot(x, y, transform=ccrs.Geodetic(), color='red', linewidth=5);
        plt.savefig("raw_map.png", bbox_inches='tight')

    return df


def avg_buoy_dist(buoys):
    '''info'''
    dlist = []
    iter_buoys = iter(buoys)
    next(iter_buoys)
    for i in range(len(buoys)-1):
        b1 = buoys[i]
        b2 = next(iter_buoys)

        d = gdis(b1, b2).feet
        d = np.round(d, 2)
        dlist.append(d)

    avg_dist = np.mean(dlist).round(2)
    return avg_dist


with open('buoy_placement.gpx') as f:
    source = f.read()

df = parse_gpx(source)


if __name__ == '__main__':
    buoys = gen_sat_map(df, place=True)
    buoys = np.array(buoys.values)

    ind = np.lexsort((buoys[:,0], buoys[:,1]))
    buoys = buoys[ind]

    print("\nSaving buoy coordinates to text file!")
    F = open("buoy_placement_coordinates.txt", 'w')
    F.write("Buoy Placement Coordinates: \n")
    for y,x in buoys:
        loc = '\n\n' + str(y) + ', ' + str(x)
        F.write(loc)
    F.close()

    avg_buoy_dist = avg_buoy_dist(buoys)

    dist_message = f"\nThe average distance from buoy-to-buoy, between the {len(buoys)} buoys, is {avg_buoy_dist}ft!"
    with open('buoy_placement_coordinates.txt', 'a') as f:
        f.write('\n\n')
        f.write(dist_message)

    print(dist_message)


else:
    gen_sat_map(df, place=False)


print("\nDONE")
