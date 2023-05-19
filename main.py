import folium
import pandas as pd


def style_function(color_high='red', color_medium='blue', color_low='green', value_low=0, value_high=1):
         return lambda x: {'fillColor': color_high if x['properties']['AREA'] >= value_high
                             else (color_low if x['properties']['AREA'] <= value_low else color_medium)}



data = pd.read_csv('capitals.txt')
capital_latitude = data['Capital Latitude']
capital_longitude = data['Capital Longitude']
capital_country_name = data['Country Name']
capital_capital_name = data['Capital Name']


map = folium.Map(location=[52.25, 21], zoom_start=6, tiles='Stamen Terrain')


fga = folium.FeatureGroup(name='Areas')


fga.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
                    style_function=style_function(value_low=50000, value_high=150000)))


fgc = folium.FeatureGroup(name='Capitals')

for la, lo, cc, cn in zip(capital_latitude, capital_longitude, capital_country_name, capital_capital_name):
    fgc.add_child(folium.CircleMarker(location=[la, lo], popup=str(cc) + '\n' + str(cn), radius=5, fill_color='red',
                                    color='red', fill_opacity=0.5))


print(help(folium.CircleMarker))

map.add_child(fgc)
map.add_child(fga)
map.add_child(folium.LayerControl())

map.save('Map1.html')
