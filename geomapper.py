import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



with open("2014_10_20.json") as f:
    source = f.read()

hike_data = json.loads(source)
hike_data = hike_data['data'][0]
hike_values = hike_data['values']
hike_fields = hike_data['fields']

clean_data = [dict(zip(hike_fields, v)) for v in hike_values]
df_data = pd.DataFrame(columns=hike_fields, data=hike_values)

'''
# Toying with & learning mapping frameworks

import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
from cartopy.io.img_tiles import OSM
import cartopy.feature as cfeature
from cartopy.io import shapereader
from cartopy.io.img_tiles import StamenTerrain
from cartopy.io.img_tiles import GoogleTiles
from owslib.wmts import WebMapTileService
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patheffects as PathEffects
import matplotlib.patches as mpatches



plt.figure(figsize=(10,10))
stamen_terrain = cimgt.StamenTerrain()
ax = plt.axes(projection=stamen_terrain.crs)
ax.set_extent((-80.127383, -80.095359, 26.911549, 26.883035))
ax.add_image(stamen_terrain, 8)

plt.show()


plt.figure(figsize=(10,10))


fig = plt.figure(figsize=(20,20))

imagery = OSM()

ax = plt.axes(projection=imagery.crs, )
ax.set_extent((-80.127383, -80.095359, 26.911549, 26.883035))

    # Add the imagery to the map.
zoom = 20
ax.add_image(imagery, zoom)

plt.title('Open Street Map and Cartopy')
plt.show()
'''
