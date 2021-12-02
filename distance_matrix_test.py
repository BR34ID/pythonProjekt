import folium
from shapely import wkt, geometry
from openrouteservice import client, places, distance_matrix
from geopy.geocoders import Nominatim
import time

api_key = '5b3ce3597851110001cf6248580243e4566c4ed28a1f498ab3b27852' #Sophies API KEY
wkt_str = 'Polygon ((13.43926404 52.48961046, 13.42040115 52.49586382, 13.42541101 52.48808523, 13.42368155 52.48635829, 13.40788599 52.48886084, 13.40852944 52.487142, 13.40745989 52.48614988, 13.40439187 52.48499746, 13.40154731 52.48500125, 13.40038591 52.48373202, 13.39423818 52.4838664, 13.39425346 52.48577149, 13.38629096 52.48582648, 13.38626853 52.48486362, 13.3715694 52.48495055, 13.37402099 52.4851697, 13.37416365 52.48771105, 13.37353615 52.48798191, 13.37539925 52.489432, 13.37643416 52.49167597, 13.36821531 52.49333093, 13.36952826 52.49886974, 13.37360623 52.50416333, 13.37497726 52.50337776, 13.37764916 52.5079675, 13.37893813 52.50693045, 13.39923153 52.50807711, 13.40022883 52.50938108, 13.40443425 52.50777471, 13.4052848 52.50821063, 13.40802944 52.50618019, 13.40997081 52.50692569, 13.41152096 52.50489127, 13.41407284 52.50403794, 13.41490921 52.50491634, 13.41760145 52.50417013, 13.41943091 52.50564912, 13.4230412 52.50498109, 13.42720031 52.50566607, 13.42940229 52.50857222, 13.45335235 52.49752496, 13.45090795 52.49710803, 13.44765912 52.49472124, 13.44497623 52.49442276, 13.43926404 52.48961046))'
ors = client.Client(key=api_key)

app = Nominatim(user_agent="tutorial")

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
pubs_coords = []

for s in addresses:
    location = get_location_by_address(s)
    latitude = location["lat"]
    longitude = location["lon"]
    print(f"{latitude}, {longitude}")
    pubs_coords.append([longitude, latitude])

request = {'locations': pubs_coords,
           'profile': 'driving-car',
           'metrics': ['distance']}

pubs_matrix = ors.distance_matrix(**request)
print("Calculated {}x{} routes.".format(len(pubs_matrix['distances']), len(pubs_matrix['distances'][0])))
print(pubs_matrix)