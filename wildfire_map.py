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
#alternative map option below
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
                       color_discrete_sequence=["red"], zoom=0, height=300)
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

#https://github.com/prof-rossetti/intro-to-python/blob/a48e76412a9c84de948698d1bf0d557551626570/exercises/codebase-cleanup/starter/app/unemployment_email.py
# https://plotly.com/python/static-image-export/

##FOR NEW WILDFIRE COUNT USE BELOW CODE
from datetime import date

df[['date','time']] = df['date'].str.split('T', expand=True) #>https://datascienceparichay.com/article/pandas-split-column-by-delimiter/#:~:text=Split%20column%20by%20delimiter%20into,True%20to%20the%20expand%20parameter.
dict = df.to_dict(orient = 'records')

wildfires_today = []
count = 0
for event in dict:
   if event['date'] == "2022-08-05":
     count += 1
     wildfires_today.append(event)
#delete below if doesn't work
wildfires_today_details = []
for info in wildfires_today:
  wildfires_today_details.append(info['title'] and ":" and info['coordinates']) 

if not os.path.exists("images"):
    os.mkdir("images")

img_filepath = os.path.join(os.path.dirname(__file__), "images", "", "wildfire.png")
fig.write_image(img_filepath)

# with attachment: https://www.twilio.com/blog/sending-email-attachments-with-twilio-sendgrid-python

import base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition, ContentId

load_dotenv()

# obtain api key at https://sendgrid.com/
# and verify single sender with a given email address...
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_ADDRESS = os.getenv("SENDER_ADDRESS")


#prep email
subject="Daily Wildfire Tracker"
html= """\
    <html>
    <head></head>
  <body>
    <p>Attached is a static image of the current wildfire map to reference for latest changes.<br>
       Please visit the map locally on your work desktop for an interactive version.<br>
       Number of wildfires started today: """ +str(count)+ """ <br>
       """ +str(wildfires_today_details)+ """
    </p>
  </body>
</html>
""" #source: https://stackoverflow.com/questions/41857610/use-a-variable-inside-html-email


client = SendGridAPIClient(SENDGRID_API_KEY) #> <class 'sendgrid.sendgrid.SendGridAPIClient>
message = Mail(
    from_email=SENDER_ADDRESS,
    to_emails=SENDER_ADDRESS,
    subject=subject,
    html_content=html
)

# for binary files, like PDFs and images:
with open(img_filepath, 'rb') as f:
    data = f.read()
    f.close()
encoded_img = base64.b64encode(data).decode()

# attach the file:
message.attachment = Attachment(
    file_content = FileContent(encoded_img),
    file_type = FileType('image/png'),
    file_name = FileName('wildfire.png'),
    disposition = Disposition('attachment'),
    content_id = ContentId('Attachment 1')
)

#send email
response = client.send(message)
print(response.status_code)