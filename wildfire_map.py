import os
from dotenv import load_dotenv #https://github.com/prof-rossetti/intro-to-python/blob/b7bbb37445bab12ee0c655a9d34658d9266db0d8/notes/python/packages/dotenv.md
load_dotenv()
api_key=os.getenv("api_key", default="demo")

import requests

nasa_url = "https://eonet.gsfc.nasa.gov/api/v2.1/categories/8?status=open&api_key={api_key}"
x = requests.get(nasa_url)

import json

data = json.loads(x.text)
#print(type(data))
#print(data)

rows = [] #https://www.tutorialspoint.com/python-convert-list-of-nested-dictionary-into-pandas-dataframe#

for fire in data['events']:
  #print(fire["title"], ":", fire["geometries"][0]["coordinates"])
  fire_row = fire['geometries']
  n = fire['title']

  for row in fire_row:
    row['title'] = n
    rows.append(row)

import plotly.graph_objects as go
import pandas as pd
import plotly.express as px

df = pd.DataFrame(rows)

split_df = pd.DataFrame(df['coordinates'].tolist(), columns=['longitude', 'latitude'])  #https://datascienceparichay.com/article/split-pandas-column-of-lists-into-multiple-columns/

df = pd.concat([df, split_df], axis=1)
#df
# https://colab.research.google.com/drive/1oFYdpTah2IYDZqdYOfpWc0poEQW2SKJy?usp=sharing#scrollTo=ZMyUY7XihNta
#fig = go.Figure(data=go.Scattergeo(
#        lon = df['longitude'],
#        lat = df['latitude'],
#        text = df['title'],
#        mode = 'markers',
#        marker=go.scattergeo.Marker(
#            size=6
 #       )
#))

#fig.update_layout(
#        title = 'Global Wildfire Tracker',
#        title_x=0.5
#    )
#fig.show()

#sattelite map
fig = px.scatter_mapbox(df, lat='latitude', lon='longitude', hover_name='title', hover_data= ['date'],
                       color_discrete_sequence=["red"], zoom=1.5, height=300)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":25,"t":25,"l":25,"b":25})
fig.update_layout(
    title = 'Global Wildfire Tracker',
    title_x = .5,
    mapbox_style="white-bg",
    mapbox_layers=[
     {
            "below": 'traces',
            "sourcetype": "raster",
            "sourceattribution": "United States Geological Survey",
            "source": [
                "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
        ]}])
fig.show()

