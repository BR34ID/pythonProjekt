from tkinter import *
import requests
from or_tools_test import Solver
import threading
import urllib.parse
from distance_matrix_generator import DistanceMatrixGenerator
from visualize_solution import build_request, make_request, startVisualizing


class TSP_GUI:

    URL_PREFIX = 'https://nominatim.openstreetmap.org/search?q='
    URL_SUFFIX = "&format=jsonv2"

    # GUI Init
    def __init__(self, mainW):
        self.distanceMatrixGenerator = None
        self.create_labels(mainW)
        self.adresslist = []  # um Adressen für Distanzmatrix vorzubereiten
        self.labels = []
        self.distance_matrix = []

        # Entry Felder für Adresseingabe
        self.adressEingabefeld = Entry(mainW)
        self.adressEingabefeld.pack()
        self.fenster = mainW
        # Button für mehr Adressfelder
        self.adresseHinzufuegenButton = Button(mainW, text="Adresse hinzufügen", command=self.is_vaild_adress)
        self.adresseHinzufuegenButton.pack()
        # Button zum Löschen der Adressen
        self.alleAdressenLoeschenButton = Button(mainW, text="Adressen löschen", command=self.clear_list)
        self.alleAdressenLoeschenButton.pack()

        # Button für Submit
        self.routeErzeugenButton = Button(mainW, text="Route erzeugen!", command=self.solve)
        self.routeErzeugenButton.pack()

        mainW.title('Routenplaner')

    # Erstellt Label
    def create_labels(self, fenster):
        Label(fenster, text="Rotenplaner Deluxe", font=("Arial", 20)).pack()
        Label(fenster, text="von Sophie R., Svea-Nele J., Niklas L.", font=("Arial", 14, "italic")).pack()
        Label(fenster, text="Bitte geben Sie Ihre Zieladressen ein.").pack()
        self.hinweisText = Label(fenster, text="Bestätigen Sie die Eingabe mit dem Button.")
        self.hinweisText.pack()

    # Funktion für mehr Adressfelder (btnMoreAddresses)
    def is_vaild_adress(self):
        if (isinstance(self.adressEingabefeld.get(), str)):
            if(self.is_adresse_valide()):
                self.add_adress()
            else:
                self.show_error("Adressvalidierung fehlgeschlagen")
        else:
            self.show_error("Bitte geben Sie eine gültige Adresse ein.")
    # Zeigt einen Fehler beim Hinweislabel an
    def show_error(self, text):
        self.hinweisText.config(text=text)

    # Fügt eine Adresse zur Adressenliste hinzu
    def add_adress(self):
        self.hinweisText.config(text="Adresse hinzugefügt.")
        self.adresslist.append(self.adressEingabefeld.get())
        label = Label(self.fenster, text=" ● " + self.adressEingabefeld.get())
        label.pack()
        self.labels.append(label)
        self.adressEingabefeld.delete(0, END)

    #Prüft ob eine eingegebene Adresse valide ist (Return true wenn valide, false wenn nicht)
    def is_adresse_valide(self):
        parsed_adress = urllib.parse.quote(self.adressEingabefeld.get(), safe="")
        url = TSP_GUI.URL_PREFIX + parsed_adress + TSP_GUI.URL_SUFFIX
        response = requests.get(url, auth=('user', 'pass'))
        return str(response.content) != "b'[]'"

    #Lösung des TSPs
    def solve(self):
        self.distanceMatrixGenerator = DistanceMatrixGenerator(adressList=self.adresslist)

        #Visualisiert die Lösung wenn möglich
        def visualize_solution(solver):
            if(len(self.distanceMatrixGenerator.adressList) > 4):
                return
            url = build_request(solver.getSolutionNodes(), self.distanceMatrixGenerator)
            make_request(url, self.distanceMatrixGenerator)
            startVisualizing()
        #Funktion zum asynchronem Lösen des Problems
        def run_async(solver):
            solver.getSolution()
            visualize_solution(solver)

        solver = Solver(self.distanceMatrixGenerator)
        threading.Thread(target=run_async(solver)).start()

    #Löscht die Adressenliste
    def clear_list(self):
        self.adresslist.clear()
        for lbl in self.labels:
            lbl.after(100, lbl.destroy())

app = Tk()
ma = TSP_GUI(app)
app.mainloop()