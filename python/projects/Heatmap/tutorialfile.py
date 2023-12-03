import pandas as pd
import plotly.express as px

# Data with latitude/longitude and values
df = pd.read_csv('https://raw.githubusercontent.com/R-CoderDotCom/data/main/sample_datasets/population_galicia.csv')

fig = px.density_mapbox(df, lat = 'latitude', lon = 'longitude', z = 'tot_pob',
                        radius = 8,
                        center = dict(lat = 42.83, lon = -8.35),
                        zoom = 6,
                        mapbox_style = 'open-street-map')
fig.show()
