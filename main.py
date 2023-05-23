import folium
import pandas as pd

## 1NO. CLASS ##


class CapitalAreaMap:

    def __init__(self, capitals_file_name, start_location, zoom_start, area_value_low, area_value_high):
        self.capitals_name = capitals_file_name
        self.start_location = start_location
        self.zoom_start = zoom_start
        self.area_value_low = area_value_low
        self.area_value_high = area_value_high
        self.capital_details = self.read_csv()
        self.map = self.make_map()
        self.area_layer = self.make_areas_layer()
        self.capital_layer = self.make_capital_layer()

    def make_map(self):
        return folium.Map(location=self.start_location, zoom_start=self.zoom_start, tiles='Stamen Terrain')

    def style_function(self, color_high='red', color_medium='blue', color_low='green'):
        return lambda x: {'fillColor': color_high if x['properties']['AREA'] >= self.area_value_high
                            else (color_low if x['properties']['AREA'] <= self.area_value_low else color_medium)}

    def make_areas_layer(self, name='Areas'):
        fg = folium.FeatureGroup(name)
        fg.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
                                                                                style_function=self.style_function()))
        return fg

    def make_capital_layer(self, name='Capitals'):
        fg = folium.FeatureGroup(name)
        for la, lo, cc, cn in zip(self.capital_details['capital_latitude'],
                                  self.capital_details['capital_longitude'],
                                  self.capital_details['capital_country_name'],
                                  self.capital_details['capital_capital_name']):
            fg.add_child(folium.CircleMarker(location=[la, lo], popup=str(cc) + '\n' + str(cn), radius=5,
                                             fill_color='red', color='red', fill_opacity=0.5))
        return fg

    def read_csv(self):
        data = pd.read_csv(self.capitals_name)
        capital_latitude = data['Capital Latitude']
        capital_longitude = data['Capital Longitude']
        capital_country_name = data['Country Name']
        capital_capital_name = data['Capital Name']
        capital_details = {'capital_latitude': capital_latitude, 'capital_longitude': capital_longitude,
                           'capital_country_name': capital_country_name, 'capital_capital_name': capital_capital_name}
        return capital_details

    def save_map(self, name='Map2'):
        self.map.add_child(self.area_layer)
        self.map.add_child(self.capital_layer)
        self.map.add_child(folium.LayerControl())
        self.map.save(name+'.html')


mapa = CapitalAreaMap(capitals_file_name='capitals.txt', start_location=[52.25, 21], zoom_start=6, area_value_low=50000,
                  area_value_high=150000)
mapa.save_map()


## 2NO. STRUCTURAL ##

#
# def style_function(color_high='red', color_medium='blue', color_low='green', value_low=0, value_high=1):
#          return lambda x: {'fillColor': color_high if x['properties']['AREA'] >= value_high
#                              else (color_low if x['properties']['AREA'] <= value_low else color_medium)}
#
#
#
# data = pd.read_csv('capitals.txt')
# capital_latitude = data['Capital Latitude']
# capital_longitude = data['Capital Longitude']
# capital_country_name = data['Country Name']
# capital_capital_name = data['Capital Name']
#
#
# map = folium.Map(location=[52.25, 21], zoom_start=6, tiles='Stamen Terrain')
#
#
# fga = folium.FeatureGroup(name='Areas')
#
#
# fga.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
#                     style_function=style_function(value_low=50000, value_high=150000)))
#
#
# fgc = folium.FeatureGroup(name='Capitals')
#
# for la, lo, cc, cn in zip(capital_latitude, capital_longitude, capital_country_name, capital_capital_name):
#     fgc.add_child(folium.CircleMarker(location=[la, lo], popup=str(cc) + '\n' + str(cn), radius=5, fill_color='red',
#                                     color='red', fill_opacity=0.5))
#
#
# print(help(folium.CircleMarker))
#
# map.add_child(fgc)
# map.add_child(fga)
# map.add_child(folium.LayerControl())
#
# map.save('Map1.html')
