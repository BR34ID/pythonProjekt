'''import requests
r = requests.get("http://router.project-osrm.org/table/v1/driving/13.388860,52.517037;13.397634,52.529407;13.428555,52.523219")

print('Status Code:')
print(r)'''

from geopy.geocoders import Nominatim
import time
from pprint import pprint

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

for s in addresses:
    location = get_location_by_address(s)
    latitude = location["lat"]
    longitude = location["lon"]
    print(f"{latitude}, {longitude}")