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

