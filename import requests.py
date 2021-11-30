'''import requests
r = requests.get("http://router.project-osrm.org/table/v1/driving/13.388860,52.517037;13.397634,52.529407;13.428555,52.523219")

print('Status Code:')
print(r)'''

from geopy.geocoders import Nominatim
import time
from pprint import pprint

app = Nominatim(user_agent="tutorial")

print("number one")

location = app.geocode("Nairobi, Kenya").raw

pprint(location)

print("number two")

'''def get_location_by_address(address):
    """This function returns a location as raw from an address
    will repeat until success"""
    time.sleep(1)
    try:
        return app.geocode(address).raw
    except:
        return get_location_by_address(address)

address = "Makai Road, Masaki, Dar es Salaam, Tanzania"
location = get_location_by_address(address)

pprint(location)

print("hello")'''


