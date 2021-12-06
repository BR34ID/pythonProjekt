import tkinter as tk

app = tk.Tk()


app.title('Routenplaner')
label1 = tk.Label(app, text="Customized Label 1", font=("Times", 20), bg="gray", fg="red")
label2 = tk.Label(app, text="Customized Label 2", font=("Times", 20, "italic"))

label1.pack()
label2.pack()

#führt bei mir zu nur schwarzem Fenster. Neue Python Version 3.10 heruntergeladen.
app.mainloop()