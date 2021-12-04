from openrouteservice import client
from geopy.geocoders import Nominatim
import time

api_key = '5b3ce3597851110001cf6248580243e4566c4ed28a1f498ab3b27852' #Sophies API KEY
ors = client.Client(key=api_key)
app = Nominatim(user_agent="TH_WILDAU_PYTHON_TSP")

#gibt eine location basierend auf der Adresse aus
def get_location_by_address(address):
    time.sleep(1)
    try:
        return app.geocode(address).raw
    except:
        return get_location_by_address(address)

def get_adress_coords(adress):
    location = get_location_by_address(adress)
    return [location["lon"], location["lat"]]

def generate_distance_matrix(adresses_list):
    pubs_coords = []
    for adress in adresses_list:
        pubs_coords.append(get_adress_coords(adress))
    request = {'locations': pubs_coords,
           'profile': 'driving-car',
           'metrics': ['distance']}
    response = ors.distance_matrix(**request)
    print("Calculated {}x{} routes.".format(len(response['distances']), len(response['distances'][0])))
    print(response['distances'])
    return response['distances']