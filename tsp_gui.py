import tkinter as tk

class TSP_GUI:
    def __init__(self,mainW):
        self.lbl1 = tk.Label(mainW, text="Rotenplaner Deluxe", font=("Arial",20))
        self.lbl2 = tk.Label(mainW, text="von Sophie R., Svea-Nele J., Niklas L.", font=("Arial", 14, "italic"))

        self.lbl3 = tk.Label(mainW, text="Bitte geben Sie Ihre Zieladressen ein.")

        mainW.title('Routenplaner')

        self.lbl1.pack()
        self.lbl2.pack()
        self.lbl3.pack()



    
#führte bei mir zu nur schwarzem Fenster. Neue Python Version 3.10 heruntergeladen.
app = tk.Tk()
ma = TSP_GUI(app)
app.mainloop()