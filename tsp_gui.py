from tkinter import *
import requests
from or_tools_test import getSolution
import threading
import urllib.parse

adresslist = []  # um Adressen für Distanzmatrix vorzubereiten
labels = []


class TSP_GUI:
    def __init__(self, mainW):
        self.createLabels(mainW)

        # Entry Felder für Adresseingabe
        self.adressEingabefeld = Entry(mainW)
        self.adressEingabefeld.pack()
        self.fenster = mainW
        # Button für mehr Adressfelder
        self.adresseHinzufuegenButton = Button(mainW, text="Adresse hinzufügen", command=self.addAddress)
        self.adresseHinzufuegenButton.pack()
        # Button zum Löschen der Adressen
        self.alleAdressenLoeschenButton = Button(mainW, text="Adressen löschen", command=self.clearList)
        self.alleAdressenLoeschenButton.pack()

        # Button für Submit
        self.routeErzeugenButton = Button(mainW, text="Route erzeugen!", command=self.submit)
        self.routeErzeugenButton.pack()

        mainW.title('Routenplaner')

    def createLabels(self, fenster):
        Label(fenster, text="Rotenplaner Deluxe", font=("Arial", 20)).pack()
        Label(fenster, text="von Sophie R., Svea-Nele J., Niklas L.", font=("Arial", 14, "italic")).pack()
        Label(fenster, text="Bitte geben Sie Ihre Zieladressen ein.").pack()
        self.hinweisText = Label(fenster, text="Bestätigen Sie die Eingabe mit dem Button.")
        self.hinweisText.pack()

    # Funktion für mehr Adressfelder (btnMoreAddresses)
    def addAddress(self):
        if (isinstance(self.adressEingabefeld.get(), str)):
            if(self.is_adressen_valide()):
                self.fuege_adresse_hinzu()
            else:
                self.zeige_fehler_an("Adressvalidierung fehlgeschlagen")
        else:
            self.zeige_fehler_an("Bitte geben Sie eine gültige Adresse ein.")

        # fügt Adresse zu Liste hinzu und Prüft ob Adresse erkannt

        print(adresslist)

    def zeige_fehler_an(self, text):
        self.hinweisText.config(text=text)

    def fuege_adresse_hinzu(self):
        print("adresse hinzugefügt")
        self.hinweisText.config(text="Adresse hinzugefügt.")
        adresslist.append(self.adressEingabefeld.get())
        label = Label(self.fenster, text=" ● " + self.adressEingabefeld.get())
        label.pack()  # you can use a bullet point emoji.
        labels.append(label)
        self.adressEingabefeld.delete(0, END)

    def is_adressen_valide(self):
        print(type(self.adressEingabefeld.get()))
        query = urllib.parse.quote(self.adressEingabefeld.get(), safe="")
        urlPrefix = 'https://nominatim.openstreetmap.org/search?q='
        urlSuffix = "&format=jsonv2"
        url = urlPrefix + query + urlSuffix
        print("url=" + url)
        r = requests.get(url, auth=('user', 'pass'))
        r.status_code
        print(str(r.content) != "b'[]'")
        return str(r.content) != "b'[]'"

    def submit(self):
        def runAsync():
            getSolution(adresslist)
            self.routeErzeugenButton.config(state="normal")

        threading.Thread(target=runAsync).start()
        self.routeErzeugenButton.config(state="disabled")

    def clearList(self):
        adresslist.clear()
        for lbl in labels:
            lbl.after(100, lbl.destroy())
        print(adresslist)


# führte bei mir zu nur schwarzem Fenster. Neue Python Version 3.10 heruntergeladen.
app = Tk()
ma = TSP_GUI(app)
app.mainloop()