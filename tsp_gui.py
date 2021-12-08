from tkinter import *
import requests
from or_tools_test import getSolution
import threading

adresslist = []  # um Adressen für Distanzmatrix vorzubereiten
labels = []


class TSP_GUI:
    def __init__(self, mainW):
        self.createLabels(mainW)

        # Entry Felder für Adresseingabe
        self.e1 = Entry(mainW)
        self.e1.pack()
        self.mainW = mainW
        # Button für mehr Adressfelder
        self.btnAddAddress = Button(mainW, text="Adresse hinzufügen.", command=self.addAddress)
        self.btnAddAddress.pack()
        # Button zum Löschen der Adressen
        self.btnDeleteAll = Button(mainW, text="Adressen löschen.", command=self.clearList)
        self.btnDeleteAll.pack()

        # Button für Submit
        self.btnSubmit = Button(mainW, text="Submit!", command=self.submit)
        self.btnSubmit.pack()

        mainW.title('Routenplaner')

    def createLabels(self, mainW):
        Label(mainW, text="Rotenplaner Deluxe", font=("Arial", 20)).pack()
        Label(mainW, text="von Sophie R., Svea-Nele J., Niklas L.", font=("Arial", 14, "italic")).pack()
        Label(mainW, text="Bitte geben Sie Ihre Zieladressen ein.").pack()
        self.lbl4 = Label(mainW, text="Bestätigen Sie die Eingabe mit dem Button.")
        self.lbl4.pack()

    # Funktion für mehr Adressfelder (btnMoreAddresses)
    def addAddress(self):
        if (isinstance(self.e1.get(), str)):
            self.lbl4.config(text="Adresse hinzugefügt.")
            adresslist.append(self.e1.get())

            query = '<' + self.e1.get() + '>'
            url = 'https://nominatim.openstreetmap.org/search?'
            url = url + query
            r = requests.get(url, auth=('user', 'pass'))
            r.status_code
            label = Label(self.mainW, text=" ● " + self.e1.get())
            label.pack()  # you can use a bullet point emoji.
            labels.append(label)
            self.e1.delete(0, END)
        else:
            self.lbl4.config(text="ERROR. Bitte geben Sie eine gültige Adresse ein.")

        # fügt Adresse zu Liste hinzu und Prüft ob Adresse erkannt

        print(adresslist)



    def submit(self):
        def runAsync():
            getSolution(adresslist)

        threading.Thread(target=runAsync).start()


    def clearList(self):
        adresslist.clear();
        for lbl in labels:
            lbl.after(100, lbl.destroy())
        print(adresslist)


# führte bei mir zu nur schwarzem Fenster. Neue Python Version 3.10 heruntergeladen.
app = Tk()
ma = TSP_GUI(app)
app.mainloop()