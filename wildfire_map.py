import requests

nasa_url = "https://eonet.gsfc.nasa.gov/api/v2.1/categories/8?status=open"
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

df = pd.DataFrame(rows)

split_df = pd.DataFrame(df['coordinates'].tolist(), columns=['longitude', 'latitude'])  #https://datascienceparichay.com/article/split-pandas-column-of-lists-into-multiple-columns/

df = pd.concat([df, split_df], axis=1)
#df
# https://colab.research.google.com/drive/1oFYdpTah2IYDZqdYOfpWc0poEQW2SKJy?usp=sharing#scrollTo=ZMyUY7XihNta
fig = go.Figure(data=go.Scattergeo(
        lon = df['longitude'],
        lat = df['latitude'],
        text = df['title'],
        mode = 'markers',
        marker=go.scattergeo.Marker(
            size=6
        )
))

fig.update_layout(
        title = 'Global Wildfire Tracker',
        title_x=0.5
    )
fig.show()
