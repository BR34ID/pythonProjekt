import folium
from shapely import wkt, geometry
from openrouteservice import client, places, distance_matrix
from geopy.geocoders import Nominatim
import time

api_key = '5b3ce3597851110001cf6248580243e4566c4ed28a1f498ab3b27852' #Sophies API KEY
wkt_str = 'Polygon ((13.43926404 52.48961046, 13.42040115 52.49586382, 13.42541101 52.48808523, 13.42368155 52.48635829, 13.40788599 52.48886084, 13.40852944 52.487142, 13.40745989 52.48614988, 13.40439187 52.48499746, 13.40154731 52.48500125, 13.40038591 52.48373202, 13.39423818 52.4838664, 13.39425346 52.48577149, 13.38629096 52.48582648, 13.38626853 52.48486362, 13.3715694 52.48495055, 13.37402099 52.4851697, 13.37416365 52.48771105, 13.37353615 52.48798191, 13.37539925 52.489432, 13.37643416 52.49167597, 13.36821531 52.49333093, 13.36952826 52.49886974, 13.37360623 52.50416333, 13.37497726 52.50337776, 13.37764916 52.5079675, 13.37893813 52.50693045, 13.39923153 52.50807711, 13.40022883 52.50938108, 13.40443425 52.50777471, 13.4052848 52.50821063, 13.40802944 52.50618019, 13.40997081 52.50692569, 13.41152096 52.50489127, 13.41407284 52.50403794, 13.41490921 52.50491634, 13.41760145 52.50417013, 13.41943091 52.50564912, 13.4230412 52.50498109, 13.42720031 52.50566607, 13.42940229 52.50857222, 13.45335235 52.49752496, 13.45090795 52.49710803, 13.44765912 52.49472124, 13.44497623 52.49442276, 13.43926404 52.48961046))'

aoi_geom = wkt.loads(wkt_str)  # load geometry from WKT string

aoi_coords = list(aoi_geom.exterior.coords)  # get coords from exterior ring
aoi_coords = [(y, x) for x, y in aoi_coords]  # swap (x,y) to (y,x). Really leaflet?!
aoi_centroid = aoi_geom.centroid  # Kreuzberg center for map center

m = folium.Map(tiles='Stamen Toner', location=(aoi_centroid.y, aoi_centroid.x), zoom_start=14)
folium.vector_layers.Polygon(aoi_coords,
                             color='#ffd699',
                             fill_color='#ffd699',
                             fill_opacity=0.2,
                             weight=3).add_to(m)
print("m="+str(m))
ors = client.Client(key=api_key)

aoi_json = geometry.mapping(geometry.shape(aoi_geom))
query = {'request': 'pois',
         'geojson': aoi_json,
         'filter_category_ids': [569],
         'sortby': 'distance'}
pubs = ors.places(**query)['features']  # Perform the actual request and get inner json

# Amount of pubs in Kreuzberg
print("\nAmount of pubs: {}".format(len(pubs)))
print(pubs)

query['filters_custom'] = {'smoking': ['yes']}  # Filter out smoker bars
pubs_smoker = ors.places(**query)['features']

print("\nAmount of smoker pubs: {}".format(len(pubs_smoker)))

pubs_addresses = []

for feat in pubs_smoker:
    lon, lat = feat['geometry']['coordinates']
    name = ors.pelias_reverse(point=(lon, lat))['features'][0]['properties']['name']
    popup = "<strong>{0}</strong><br>Lat: {1:.3f}<br>Long: {2:.3f}".format(name, lat, lon)
    icon = folium.map.Icon(color='lightgray',
                           icon_color='#b5231a',
                           icon='beer',  # fetches font-awesome.io symbols
                           prefix='fa')
    folium.map.Marker([lat, lon], icon=icon, popup=popup).add_to(m)
    pubs_addresses.append(name)

pubs_coords = [feat['geometry']['coordinates'] for feat in pubs_smoker]
print("pubs_coords=")
print(pubs_coords)
print(type(pubs_coords))
'''app = Nominatim(user_agent="tutorial")

#gibt eine location basierend auf der Adresse aus
def get_location_by_address(address):
    """This function returns a location as raw from an address
    will repeat until success"""
    time.sleep(1)
    try:
        return app.geocode(address).raw
    except:
        return get_location_by_address(address)

addresses = ["Berlin, Germany", "Hamburg, Germany", "Stuttgart, Germany"]
pubs_coords = {}

for s in addresses:
    location = get_location_by_address(s)
    latitude = location["lat"]
    longitude = location["lon"]
    print(f"{latitude}, {longitude}")
    pubs_coords[latitude] = longitude'''

request = {'locations': pubs_coords,
           'profile': 'driving-car',
           'metrics': ['duration']}

pubs_matrix = ors.distance_matrix(**request)
print("Calculated {}x{} routes.".format(len(pubs_matrix['durations']), len(pubs_matrix['durations'][0])))
print(pubs_matrix)