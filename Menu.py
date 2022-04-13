from tkinter import *


class Menu:
    """Αρχικό μενού, περιέχει buttons και το frame που τοποθετούνται στο master"""

    def __init__(self, master):
        self.frame = Frame(master, bg="green").place(relx=.5, rely=.5)
        # Δημιουργία Buttons
        self.b_new_game = Button(self.frame, text="Νέο Παιχνίδι", font="Verdana 26 bold", bg="grey", height=2, width=11, command=self.new_game)
        self.b_continue = Button(self.frame, text="Συνέχεια...", font="Verdana 26 bold", bg="grey", height=2, width=11)

        # Τοποθέτηση των buttons
        self.b_new_game.place(relx=.5, rely=.3, anchor='center')
        self.b_continue.place(relx=.5, rely=.45, anchor='center')

    def new_game(self):
        # Διαγραφή των προηγούμενων buttons
        self.b_new_game.destroy()
        self.b_continue.destroy()

        # Επιλογή Δυσκολίας
        dif_prompt = Label(self.frame, text="Διάλεξε Δυσκολία:", font="Verdana 26 bold", bg="green")
        dif_prompt.place(rely=.2, relx=.2)

        # Δημιουργία Buttons για επιλογή δυσκολίας
        b_easy = self.b_new_game = Button(self.frame, text="Εύκολο", font="Verdana 22 bold", bg="grey", height=1, width=11)
        b_medium = self.b_new_game = Button(self.frame, text="Μέτριο", font="Verdana 22 bold", bg="grey", height=1, width=11)
        b_hard = self.b_new_game = Button(self.frame, text="Δύσκολο", font="Verdana 22 bold", bg="grey", height=1, width=11)

        # Τοποθέτηση buttons για δυσκολια
        b_easy.place(relx=.5, rely=.3, anchor='center')
        b_medium.place(relx=.5, rely=.38, anchor='center')
        b_hard.place(relx=.5, rely=.46, anchor='center')




