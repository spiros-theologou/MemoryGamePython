from Memory_game import *


class Menu:
    """Μενού, περιέχει buttons και το frame που τοποθετούνται στο master"""

    def __init__(self, master):
        self.master = master
        self.frame = Frame(master, bg="green").place(relx=.5, rely=.5)


        # Label με μήνυμα τον τίτλο του παιχνιδιού
        self.welcome_message = Label(self.master, text="Παιχνίδι Mνήμης με Tράπουλα!",
                                bg="green", fg="red",
                                font="Verdana 36 bold italic", bd=1)
        self.welcome_message.place(relx=.5, rely=.05, anchor="n")
        # Δημιουργία Buttons
        self.b_new_game = Button(self.frame, text="Νέο Παιχνίδι", font="Verdana 26 bold", bg="grey", height=2, width=11, command=self.new_game)
        self.b_continue = Button(self.frame, text="Συνέχεια...", font="Verdana 26 bold", bg="grey", height=2, width=11)

        # Τοποθέτηση των buttons
        self.b_new_game.place(relx=.5, rely=.3, anchor='center')
        self.b_continue.place(relx=.5, rely=.45, anchor='center')

        # Αρχικοποίηση της δυσκολίας, του αριθμού παικτών και του είδους παιχνιδιού(συνέχιση τελευταίου ή έναρξη νέου)
        self.difficulty = ""
        self.players = 0
        self.mode = ""

    def new_game(self):
        self.mode = "New Game"
        print("New game")
        # Διαγραφή των προηγούμενων buttons
        self.clear_screen(self.b_new_game, self.b_continue)

        # Επιλογή Δυσκολίας
        dif_prompt = Label(self.frame, text="Διάλεξε Δυσκολία:", font="Verdana 26 bold", bg="green")
        dif_prompt.place(rely=.2, relx=.2)

        # Δημιουργία Buttons για επιλογή δυσκολίας
        b_easy = Button(self.frame, text="Εύκολο", font="Verdana 22 bold", bg="grey", height=1, width=11,
                        command=lambda: [self.clear_screen(dif_prompt, b_easy, b_medium, b_hard),
                                         self.num_of_players(),
                                         self.set_difficulty("easy")]
                        )
        b_medium = Button(self.frame, text="Μέτριο", font="Verdana 22 bold", bg="grey", height=1, width=11,
                          command=lambda: [self.clear_screen(dif_prompt, b_easy, b_medium, b_hard),
                                           self.num_of_players(),
                                           self.set_difficulty("normal")
                                           ]
                          )
        b_hard = Button(self.frame, text="Δύσκολο", font="Verdana 22 bold", bg="grey", height=1, width=11,
                        command=lambda: [self.clear_screen(dif_prompt, b_easy, b_medium, b_hard),
                                         self.num_of_players(),
                                         self.set_difficulty("hard")
                                         ]
                        )

        # και button για επιστροφη στο αρχικό μενού
        # b_back = Button(self.master, text="Πίσω", font="Verdana 18 bold", bg="grey", height=1, width=6, command=lambda: self.__init__(self.master))

        # Τοποθέτηση buttons
        b_easy.place(relx=.5, rely=.3, anchor='center')
        b_medium.place(relx=.5, rely=.38, anchor='center')
        b_hard.place(relx=.5, rely=.46, anchor='center')
        # b_back.place(relx=.1, rely=.1, anchor='nw')

    def num_of_players(self):
        """Επιλογή αριθμού παχτών"""
        choice_prompt = Label(self.frame, text="Επίλεξε Αριθμό Παιχτών:", font="Verdana 26 bold", bg="green")
        choice_prompt.place(relx=.3, rely=.3, anchor='center')
        # Αρχικοποίηση αριθμού παιχτών
        # Buttons
        b1 = Button(self.frame, text="1", font="Verdana 22 bold", bg="grey", height=1, width=4, command=lambda: [self.set_number_of_players(1),
                                                                                                                 self.clear_screen(self.welcome_message, choice_prompt, b1, b2, b3, b4),
                                                                                                                 self.start_game()])
        b2 = Button(self.frame, text="2", font="Verdana 22 bold", bg="grey", height=1, width=4, command=lambda: [self.set_number_of_players(2),
                                                                                                                 self.clear_screen(self.welcome_message, choice_prompt, b1, b2, b3, b4),
                                                                                                                 self.start_game()])
        b3 = Button(self.frame, text="3", font="Verdana 22 bold", bg="grey", height=1, width=4, command=lambda: [self.set_number_of_players(3),
                                                                                                                 self.clear_screen(self.welcome_message, choice_prompt, b1, b2, b3, b4),
                                                                                                                 self.start_game()])
        b4 = Button(self.frame, text="4", font="Verdana 22 bold", bg="grey", height=1, width=4, command=lambda: [self.set_number_of_players(4),
                                                                                                                 self.clear_screen(self.welcome_message, choice_prompt, b1, b2, b3, b4),
                                                                                                                 self.start_game()])

        # Τοποθέτηση κουμπιών
        b1.place(relx=.4, rely=.38, anchor='center')
        b2.place(relx=.5, rely=.38, anchor='center')
        b3.place(relx=.6, rely=.38, anchor='center')
        b4.place(relx=.7, rely=.38, anchor='center')

    def clear_screen(self, *widgets):
        """Αφαιρεί τα widgets από το παράθυρο"""
        for widget in widgets:
            widget.destroy()

    def set_number_of_players(self, players):
        self.players = players
        print(f"Players: {players}")

    def set_difficulty(self, dif):
        self.difficulty = dif
        print(f"Difficulty: {self.difficulty}")

    def start_game(self):
        """Καταστρέφει το frame του μενού ώστε να μπορεί να φορτωθεί το board,
         Καλεί την έναρξη παιχνιδιού"""
        if self.mode == "New Game":
            NewGame(self.master, self.difficulty, self.players)
