import sys
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
import folium
import distance_matrix_generator

m = folium.Map(location=[45.5236, -122.6750])
m.save("index.html")

#GraphHopper Request zusammenbauen
graphhopper_api_key = "b35bce5d-2540-4cd0-b030-eb5c02461d24";
request_options = "&points_encoded=false&profile=car&locale=de&key=" + graphhopper_api_key
request_base = "https://graphhopper.com/api/1/route?"
request_points = "point=51.131,12.414&point=52.520008,13.404954"
request_string = request_base + request_points + request_options


def build_request(solution_index_list):
    pointstring = ""
    print("solution_index_list")
    print(solution_index_list)
    print("+coords:")
    print(distance_matrix_generator.coords)
    pointstring += get_coords(0)#Started immer im Depot, welches der erste (=0.) eingegebene Wert ist.
    for i in solution_index_list:
        print("Koordinaten: **" + str(i))
        pointstring += get_coords(i)
    request_string_ = request_base + pointstring + request_options
    print(request_string_)
    return request_string_


def get_coords(i):
    return "point=" + distance_matrix_generator.coords[i][1] + "," + distance_matrix_generator.coords[i][0] + "&"

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