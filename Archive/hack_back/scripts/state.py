import plotly.express as px
import geopandas
import sys

gdf = geopandas.GeoDataFrame.from_file("./data/gdf.geojson")

num = sys.argv[1]

fig = px.choropleth(
    gdf,
    geojson=gdf.geometry,
    locations=gdf.index,
    color="num_of_clients_selection_" + num,
    hover_data=[gdf.name],
    color_continuous_scale="Blues",
    title="Количество клиентов в регионах",
    width=900,
    height=600,
)
fig.update_geos(
    visible=False,
    center={"lat": 64, "lon": 94},
    projection_scale=2,
)
fig.update_traces(marker_line_width=1)
fig.update_layout(
    margin={"r": 0, "l": 0, "b": 0},
)

print(fig.to_json())
