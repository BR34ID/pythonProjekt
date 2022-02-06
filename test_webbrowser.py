import sys
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
import folium
from distance_matrix_generator import DistanceMatrixGenerator

m = folium.Map(location=[52.3260146, 13.6265615])
m.save("index.html")

#GraphHopper Request zusammenbauen
GRAPHHOPPER_API_KEY = "b35bce5d-2540-4cd0-b030-eb5c02461d24";
REQUEST_OPTIONS = "&points_encoded=false&profile=car&locale=de&key=" + GRAPHHOPPER_API_KEY
REQUEST_BASE = "https://graphhopper.com/api/1/route?"
REQUEST_POINTS = "point=51.131,12.414&point=52.520008,13.404954"

def build_request(solution_index_list, distanceMatrixGenerator):
    pointstring = get_coords(distanceMatrixGenerator, 0) #Started immer im Depot, welches der erste (=0.) eingegebene Wert ist.
    for i in solution_index_list:
        pointstring += get_coords(distanceMatrixGenerator, i)
    request_string = REQUEST_BASE + pointstring + REQUEST_OPTIONS
    print(request_string)
    return request_string


def get_coords(distanceMatrixGenerator, i):
    INDEX_LONGTITUDE = 1
    INDEX_LATITUDE = 0;
    return "point=" + getCoordsFor(distanceMatrixGenerator, i, INDEX_LONGTITUDE) +\
           "," + getCoordsFor(distanceMatrixGenerator, i, INDEX_LATITUDE) + "&"

def getCoordsFor(distanceMatrixGenerator, index, coordtype):
    return distanceMatrixGenerator.coords[index][coordtype]

def read_file_as_string(filename):
    f = open(filename, 'r')
    string = f.read()
    return string;

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