import json
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.io.img_tiles import GoogleTiles


with open("2014_10_20.json") as f:
    source = f.read()

hike_dict = json.loads(source)
hike_data = hike_dict['data'][0]
hike_values = hike_data['values']
hike_fields = hike_data['fields']

clean_data = [dict(zip(hike_fields, v)) for v in hike_values]
for d in clean_data:
    d['lat'] = d['latlng'][0]
    d['lon'] = d['latlng'][1]

hike_df = pd.DataFrame(columns=hike_fields, data=hike_values)
latlng_df = pd.DataFrame(hike_df.latlng.values.tolist(), columns=['lat', 'lon'])

hikedf = pd.concat([hike_df, latlng_df], axis=1)

def main():
    img = GoogleTiles(url='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}.jpg')
    plt.figure(figsize=(100,100))
    ax = plt.axes(projection=img.crs)

    ax.set_extent([-80.127383, -80.095359, 26.911549, 26.883035])

    ax.add_image(img, 18)

    x, y = hikedf.lon, hikedf.lat

    ax.plot(x, y, transform=ccrs.Geodetic(), color='blue', linewidth=3)

    plt.savefig("test_map.png")

if __name__ == '__main__':
    main()