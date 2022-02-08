from openrouteservice import client
from geopy.geocoders import Nominatim
import time


class DistanceMatrixGenerator:
    API_KEY = '5b3ce3597851110001cf6248580243e4566c4ed28a1f498ab3b27852'  # Sophies API KEY

    def __init__(self, adressList):
        self.app = Nominatim(user_agent="TH_WILDAU_PYTHON_TSP")
        self.ors = client.Client(key=DistanceMatrixGenerator.API_KEY)
        self.distance_matrix = []
        self.coords = [[]]
        self.adressList = adressList

    # gibt eine Lokation (als Koordinaten) basierend auf der schriftlichen Adresse aus
    def get_location_by_address(self, address):
        time.sleep(1)
        try:
            return self.app.geocode(address).raw
        except:
            return self.get_location_by_address(address)

    def get_adress_coords(self, adress):
        location = self.get_location_by_address(adress)
        return [location["lon"], location["lat"]]

    #Generiert die Distanzmatrix
    def generate_distance_matrix(self):
        self.coords = self.generate_coordinates_list()
        request = {'locations': self.coords,
                   'profile': 'driving-car',
                   'metrics': ['distance']}
        response = self.ors.distance_matrix(**request)
        self.distance_matrix = response['distances']
        return self.distance_matrix

    #Löst die Adressenliste in eine Koordinatenliste auf
    def generate_coordinates_list(self):
        coordslist = []
        for adress in self.adressList:
            coordslist.append(self.get_adress_coords(adress))
        return coordslist

    #Getter Funktion für die Adressenliste
    def getAdresses(self):
        return self.adressList
