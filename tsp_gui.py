import tkinter as tk

class TSP_GUI:
    def __init__(self,mainW):
        self.lbl1 = tk.Label(mainW, text="Rotenplaner Deluxe", font=("Arial",20))
        self.lbl2 = tk.Label(mainW, text="von Sophie R., Svea-Nele J., Niklas L.", font=("Arial", 14, "italic"))

        self.lbl3 = tk.Label(mainW, text="Bitte geben Sie Ihre Zieladressen ein.")

        #Entry Felder für Adresseingabe
        self.e1 = tk.Entry(mainW)
        self.e2 = tk.Entry(mainW)
        self.e3 = tk.Entry(mainW)
        self.e4 = tk.Entry(mainW) #wird erst durch Button aktiviert

        #Button für mehr Adressfelder
        self.btnMoreAddresses = tk.Button(mainW, text="Say hello", command=self.moreAddresses)

        #Button für Submit
        self.btnSubmit = tk.Button(mainW, text="Submit!", command=self.submit)

        mainW.title('Routenplaner')

        self.lbl1.pack()
        self.lbl2.pack()
        self.lbl3.pack()
        self.e1.pack()
        self.e2.pack()
        self.e3.pack()
        self.btnMoreAddresses.pack()
        self.btnSubmit.pack()

    #Funktion für mehr Adressfelder (btnMoreAddresses)
    def moreAddresses(self):
         self.e4.pack() #dynamisch machen?? 

    def submit(self):
        self.lbl3.config(text="Hallo.")


    
#führte bei mir zu nur schwarzem Fenster. Neue Python Version 3.10 heruntergeladen.
app = tk.Tk()
ma = TSP_GUI(app)
app.mainloop()