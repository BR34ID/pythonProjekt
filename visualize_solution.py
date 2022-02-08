import sys
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
import folium
import requests
#Erstellen der initialen Map mit Berlin als Startpunkt
m = folium.Map(location=[52.3260146, 13.6265615])

#GraphHopper Request zusammenbauen
GRAPHHOPPER_API_KEY = "b35bce5d-2540-4cd0-b030-eb5c02461d24";
REQUEST_OPTIONS = "&points_encoded=false&profile=car&locale=de&key=" + GRAPHHOPPER_API_KEY
REQUEST_BASE = "https://graphhopper.com/api/1/route?"

#Erstellt die Request-URL
def build_request(solution_index_list, distanceMatrixGenerator):
    pointstring = get_coords(distanceMatrixGenerator, 0) #Started immer im Depot, welches der erste (=0.) eingegebene Wert ist.
    for i in solution_index_list:
        pointstring += get_coords(distanceMatrixGenerator, i)
    request_string = REQUEST_BASE + pointstring + REQUEST_OPTIONS
    print(request_string)
    return request_string

#Führt die Request aus und zeichnet die Linie/Marker auf die Map
def make_request(requesturl, distanceMatrixGenerator):
    response = requests.get(requesturl).json()
    reversedCoords = []
    for coordinates in response['paths'][0]['points']['coordinates']:
        reversedCoords.append([coordinates[1], coordinates[0]])
    folium.PolyLine(reversedCoords, color="red", weigth=2.5, opacity=1).add_to(m)
    for point in distanceMatrixGenerator.coords:
        folium.Marker([point[1], point[0]]).add_to(m)
    m.save("index.html")

#Holt sich die Koordinaten für den Index i
def get_coords(distanceMatrixGenerator, i):
    INDEX_LONGTITUDE = 1
    INDEX_LATITUDE = 0
    return "point=" + getCoordsFor(distanceMatrixGenerator, i, INDEX_LONGTITUDE) +\
           "," + getCoordsFor(distanceMatrixGenerator, i, INDEX_LATITUDE) + "&"

def getCoordsFor(distanceMatrixGenerator, index, coordtype):
    return distanceMatrixGenerator.coords[index][coordtype]

#Liest eine Datei als String aus
def read_file_as_string(filename):
    f = open(filename, 'r')
    string = f.read()
    return string

#Startet die GUI für die Visualisierung
def startVisualizing():
    class MainWindow(QMainWindow):
        def __init__(self):
            super(MainWindow, self).__init__()
            self.browser = QWebEngineView()
            self.browser.setHtml(read_file_as_string("index.html"))
            self.setCentralWidget(self.browser)
            self.showMaximized()

    app = QApplication(sys.argv)
    QApplication.setApplicationName('Lösung:')
    window = MainWindow()
    app.exec_()