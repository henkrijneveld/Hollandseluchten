import pandas as pd
import plotly.express as px

# Data with latitude/longitude and values
#df = pd.read_csv('https://raw.githubusercontent.com/R-CoderDotCom/data/main/sample_datasets/population_galicia.csv')

#data = {'lat': [52.469, 52.471, 52.475, 52.305], 'lon': [4.641, 4.810, 4.820, 5.115], "pm25": [10, 120.5, 75, 15]}
data = {'lat': [52.469, 52.471, 52.481, 52.305], 'lon': [4.641, 4.810, 4.810, 5.115],
        "pm25": [7.5, 20, 20, 15], "size": [20, 20, 20, 20]}

df = pd.DataFrame(data=data)

#fig = px.density_mapbox(df, lat = 'latitude', lon = 'longitude', z = 'tot_pob',
#                        radius = 8,
#                        center = dict(lat = 42.83, lon = -8.35),
#                        zoom = 6,
#                        mapbox_style = 'open-street-map')


#fig = px.density_mapbox(df, lat = 'lat', lon = 'lon', z = 'pm25',
#                        radius = 30,
#                        center = dict(lat = 52.471, lon = 4.810),
#                        zoom = 9,
#                        mapbox_style = 'open-street-map',
#                        range_color = (5, 25),
#                        opacity = 0.75
#                        )



fig = px.scatter_mapbox(df, lat = 'lat', lon = 'lon', color = 'pm25',
                        center = dict(lat = 52.471, lon = 4.810),
                        zoom = 9,
#                        mapbox_style = 'open-street-map',
                        mapbox_style='carto-darkmatter',
                        range_color = (5, 25),
                        opacity = 0.5,
                        size = "pm25",
                        size_max = 20,
                        )

fig.show()
