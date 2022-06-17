from Memory_game import *
from class_Computer import Computer  # για τη δημιουργία του AI Παίκτη


class ContinueGame(NewGame):
    """Κλάση ContinueGame που καλείται όταν πατάμε το κουμπί συνέχεια στο αρχικό μενού.
     Κληρονομεί και χρησιμοποιεί μεθόδους από το NewGame
     Ανακατασκευάζει το board, scoreboard και γενικότερα το παιχνίδι,
     με δεδομένα που παίρνει από το αρχείο 'saved_game_data' """

    def __init__(self, f, master):

        self.master = master

        self.computer = None

        # ανοίγουμε το αρχείο, έχει γίνει έλεγχος στο Menu για την ύπαρξή του
        with open(f, "rb") as infile:
            self.current_state = pickle.load(infile)

        # εξαγωγή των απαιτούμενων στοιχείων για το reconstruction του παιχνιδιού
        self.extract_data()
        self.current_player = self.players[self.current_player_index]

        # Δημιουργία του frame που θα τοποθετηθεί η λεζάντα των μηνυμάτων παιχνιδιού(ποιος παίζει, αν έχουμε match η όχι κλπ...)
        self.message_frame = Frame(master, bg="green")
        self.message_frame.columnconfigure(index=0, weight=1)
        self.message_frame.rowconfigure(index=0, weight=1)
        self.message_frame.place(relx=0.5, rely=0.5, anchor="n")

        # Δημιουργία του frame και καθορισμός του grid για το board
        self.board_frame = Frame(master, bg="green")
        self.board_frame.columnconfigure(index=0, weight=1)
        self.board_frame.rowconfigure(index=0, weight=1)
        self.board_frame.place(relx=.5, rely=.5, anchor="center")

        # Δημιουργία του frame που θα τοποθετηθεί το scoreboard
        self.score_frame = Frame(master, bg="green")
        self.score_frame.columnconfigure(index=0, weight=1)
        self.score_frame.rowconfigure(index=0, weight=1)
        self.score_frame.place(relx=0.08, rely=-0.005, anchor="ne")

        # κατασκευή των tiles που θα τοποθετηθούν στο board
        self.tile_reconstruction()

        # ανακατασκευή του board
        self.board_reconstruction()

        # ανακατασκευή του scoreboard
        self.create_scoreboard()

        # Δημιουργία και τοποθέτηση του message_board
        self.create_message_board()

        self.click_count = 0  # μεταβλητή που αποθηκεύει των αριθμό των κλικαρισμένων tiles ανά γύρο
        self.clicked_tiles = []  # λίστα στην οποία θα αποθηκεύονται προσωρινά τα ανοιγμένα tiles

        self.check_game_end()  # έλεγχος για το αν έχει ολοκληρωθεί το παιχνίδι

    def extract_data(self):
        """Εξάγει τα δεδομένα από το αρχείο που διαβάσαμε"""
        self.current_player_index = self.current_state.player_index
        self.tiles_info = self.current_state.tiles_info
        self.open_tiles = self.current_state.open_tiles
        self.total_tiles = self.current_state.total_tiles
        self.difficulty = self.current_state.difficulty
        self.players = self.current_state.players_list
        if self.current_state.computer_score:
            self.players.insert(0, Computer())
            self.players[0].score = self.current_state.computer_score
            self.computer = self.players[0]


    def tile_reconstruction(self):
        """Δημιουργεί τη λίστα και τα tiles που περιέχει"""
        self.tiles = []
        for tile_info in self.tiles_info:
            tile = Tile(rank=tile_info[0], suit=tile_info[1], is_flipped=tile_info[2], master=self.board_frame, bg="green", bd=0)
            if tile.is_flipped:
                # αν το tile είναι face up, ορίζουμε ως image το front image και δεν προσθέτουμε λειτουργικότητα
                tile.image = tile.front_image
                tile.configure(image=tile.image)
            else:
                tile.image = tile.back_image
                tile.configure(image=tile.image)
                tile.configure(command=lambda t=tile: self.button_click(t))
            self.tiles.append(tile)

        # δημιουργεί τη λίστα με το ιστορικό αν υπάρχει ΑΙ
        if isinstance(self.players[0], Computer):
            for index in self.current_state.computer_history_indexes:
                print(self.tiles[index])
                self.players[0].history.append(self.tiles[index])


    def board_reconstruction(self):
        """Τοποθετεί τα tiles στο board"""

        # Εύκολο
        if self.difficulty == "easy":
            columns = 4
            # Τοποθέτηση των tiles
            j = 0
            for k, tile in enumerate(self.tiles):
                tile.grid(row=j, column=k % columns, padx=15, pady=10)
                if (k + 1) % columns == 0:
                    j += 1

        # Κανονικό
        if self.difficulty == "normal":
            columns = 10
            print("Initializing Normal Board")
            # Τοποθέτηση των tiles
            j = 0
            for k, tile in enumerate(self.tiles):
                tile.grid(row=j, column=k % columns, padx=10, pady=10)
                if (k + 1) % columns == 0:
                    j += 1

        # Δύσκολο
        if self.difficulty == "hard":
            columns = 13
            # Τοποθέτηση των tiles
            j = 0
            for k, tile in enumerate(self.tiles):
                tile.grid(row=j, column=k % columns, padx=6, pady=6)
                if (k + 1) % columns == 0:
                    j += 1
