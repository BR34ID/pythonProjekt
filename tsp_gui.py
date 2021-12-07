import tkinter as tk

adresslist = [] #um Adressen für Distanzmatrix vorzubereiten

class TSP_GUI:
    def __init__(self,mainW):
        self.lbl1 = tk.Label(mainW, text="Rotenplaner Deluxe", font=("Arial",20))
        self.lbl2 = tk.Label(mainW, text="von Sophie R., Svea-Nele J., Niklas L.", font=("Arial", 14, "italic"))

        self.lbl3 = tk.Label(mainW, text="Bitte geben Sie Ihre Zieladressen ein.")
        self.lbl4 = tk.Label(mainW, text="Bestätigen Sie die Eingabe mit dem Button.")


        #Entry Felder für Adresseingabe
        self.e1 = tk.Entry(mainW)

        #Button für mehr Adressfelder
        self.btnAddAddress = tk.Button(mainW, text="Adresse hinzufügen.", command=self.addAddress)

        #Button für Submit
        self.btnSubmit = tk.Button(mainW, text="Submit!", command=self.submit)

        mainW.title('Routenplaner')

        self.lbl1.pack()
        self.lbl2.pack()
        self.lbl3.pack()
        self.e1.pack()
        self.btnAddAddress.pack()
        self.btnSubmit.pack()
        self.lbl4.pack()

    #Funktion für mehr Adressfelder (btnMoreAddresses)
    def addAddress(self):
        self.lbl4.config(text="Adresse hinzugefügt.")
        #fügt Adresse zu Liste hinzu und Prüft ob Adresse erkannt
        adresslist.append(self.e1.get())
        self.e1.delete(0,tk.END)
        print(adresslist)

    def submit(self):
        self.lbl3.config(text="Hallo.")


    
#führte bei mir zu nur schwarzem Fenster. Neue Python Version 3.10 heruntergeladen.
app = tk.Tk()
ma = TSP_GUI(app)
app.mainloop()