from class_tile import *
from random import shuffle
from class_player import Player
from time import sleep


class NewGame:
    """Κλάση New Game, δημιουργεί το board και την υλοποίηση του νέου παιχνιδιού,
     δεδομένων της δυσκολίας και του αριθμού των παιχτών"""

    def __init__(self, master, difficulty, total_players):
        self.master = master
        self.difficulty = difficulty
        self.total_players = total_players

        # Δημιουργία του frame και καθορισμός του grid για το board
        self.board_frame = Frame(master, bg="green")
        self.board_frame.columnconfigure(index=0, weight=1)
        self.board_frame.rowconfigure(index=0, weight=1)
        self.board_frame.place(relx=.5, rely=.5, anchor="center")

        # Κλήση μεθόδων για τη δημιουργία του board και την προσθήκη λειτουργικότητας στα tiles
        self.tiles = []
        self.init_tiles()
        self.create_board()
        self.add_tile_functionality()

        # Αρχικοποίηση της λίστας με τους παίκτες
        self.players = []
        self.init_players()

        # Δημιουργία του frame που θα τοποθετηθεί το scoreboard
        self.score_frame = Frame(master, bg="green")
        self.score_frame.columnconfigure(index=0, weight=1)
        self.score_frame.rowconfigure(index=0, weight=1)
        self.score_frame.place(relx=0.08, rely=-0.005, anchor="ne")



        # Δημιουργία και τοποθέτηση του scoreboard
        self.create_scoreboard()




        # Αρχικοποίηση του αριθμού του γύρου, των "γυρισμένων" tiles ανά γύρο(click_count - θα βοηθήσει στο να προσδιορίσουμε πότε τελειώνει ο γύρος για έναν παίκτη)
        # της λίστας με τα επιλεγμένα tiles ανά γύρο
        # και του index του παίκτη που παίζει
        self.current_player = self.players[0].name
        self.round = 1
        self.click_count = 0
        self.clicked_tiles = []  # λίστα στην οποία θα αποθηκεύονται προσωρινά τα ανοιγμένα tiles

        # Αρχικοποίηση του αριθμού των "ανοιχτών" και των "κλειστών" tiles
        self.open_tiles = 0
        self.closed_tiles = len(self.tiles)

    def init_tiles(self):
        """Αρχικοποιεί μια λίστα από tiles, ανάλογα με τη δυσκολία που επιλέχθηκε"""

        # Εύκολο
        if self.difficulty == "easy":  # μόνο φιγούρες και 10
            for rank in ranks:
                for suit in suits:
                    if rank in (10, "jack", "queen", "king"):
                        tile = Tile(rank=rank, suit=suit, master=self.board_frame, bg="green", bd=0)
                        self.tiles.append(tile)

        # Μέτριο
        if self.difficulty == "normal":  # όλα εκτός των φιγούρων
            for rank in ranks:
                for suit in suits:
                    if rank not in ("jack", "queen", "king"):
                        tile = Tile(rank=rank, suit=suit, master=self.board_frame, bg="green", bd=0)
                        self.tiles.append(tile)

        # Δύσκολο
        if self.difficulty == "hard":  # όλα τα φύλλα
            for rank in ranks:
                for suit in suits:
                    tile = Tile(rank=rank, suit=suit, master=self.board_frame, bg="green", bd=0)
                    self.tiles.append(tile)

        shuffle(self.tiles)  # "ανακάτεμα" των tiles


    def button_click(self, tile):
        """Η συνάρτηση που καλείται με το κλικάρισμα ενός tile"""

        self.click_count += 1  # μετρητής των click για αυτόν το γύρο
        print(self.click_count)
        self.flip(tile)
        self.master.update()  # ανανέωση του master για εμφάνιση των ανοιχτών tiles.
        self.clicked_tiles.append(tile)
        print(self.clicked_tiles)

        # συγκρίνουμε τα tiles αν είναι 2 κλικαρισμένα
        if self.click_count == 2:
            self.compare_tiles(self.clicked_tiles)



            self.clicked_tiles.clear()
            self.click_count = 0





    def compare_tiles(self, tile_list):
        """Συγκρίνει τα tiles της λίστας και πράττει αναλόγως.."""
        if tile_list[0].rank != tile_list[1].rank:  # αν δεν ταιριάζουν, τα γυρνάμε ανάποδα
            print("NO MATCH")
            sleep(0.7)
            for t in tile_list:
                self.flip(t)
                # refresh των tiles που κλικάραμε
                for tile in self.clicked_tiles:
                    tile.configure(command=lambda t=tile: self.button_click(t))
        else:
            print("MATCH!")

    def flip(self, tile):
        """Συνάρτηση που 'γυρίζει' ένα tile"""
        if not tile.is_flipped:
            # αν το tile είναι face down, το γυρίζει και αφαιρεί τη λειτουργικότητα
            print(f"Flipping tile{repr(tile)}, {self.tiles.index(tile)}")
            tile.image = tile.front_image
            tile.flip()
            tile.configure(image=tile.image)
            tile.configure(command=0)
        else:
            if tile.is_flipped:
                print(f"Unflipping tile{repr(tile)}, {self.tiles.index(tile)}")
                tile.image = tile.back_image
                tile.flip()
                tile.configure(image=tile.image)
                tile.configure(command=lambda t=tile: self.flip(t))

    def add_tile_functionality(self):
        """ Προσθήκη λειτουργικότητας στα tiles , αλλάζοντας την εικόνα που φαίνεται στο tile που κλικάρεται"""
        for tile in self.tiles:
            tile.configure(command=lambda t=tile: self.button_click(t))

    def create_board(self):
        """Δημιουργεί  το board, ανάλογα με τη δυσκολία"""

        # Εύκολο
        if self.difficulty == "easy":
            columns = 4
            print("Initializing Easy Board")
            # Τοποθέτηση των tiles
            j = 0
            for k, tile in enumerate(self.tiles):
                print(repr(tile))  # να αφαιρεθεί, είναι βοηθητικό
                tile.image = tile.back_image
                tile.configure(image=tile.image)
                tile.grid(row=j, column=(k + 1) % columns, padx=15, pady=10)
                if (k + 1) % columns == 0:
                    j += 1

        # Κανονικό
        if self.difficulty == "normal":
            columns = 10
            print("Initializing Normal Board")
            # Τοποθέτηση των tiles
            j = 0
            for k, tile in enumerate(self.tiles):
                print(repr(tile))  # είναι βοηθητικό print
                tile.image = tile.back_image
                tile.configure(image=tile.image)
                tile.grid(row=j, column=(k + 1) % columns, padx=10, pady=10)
                if (k + 1) % columns == 0:
                    j += 1

        # Δύσκολο
        if self.difficulty == "hard":
            columns = 13
            print("Initializing Hard Board")
            # Τοποθέτηση των tiles
            j = 0
            for k, tile in enumerate(self.tiles):
                print(repr(tile))  # να αφαιρεθεί, είναι βοηθητικό
                tile.image = tile.back_image
                tile.configure(image=tile.image)
                tile.grid(row=j, column=(k + 1) % columns, padx=6, pady=6)
                if (k + 1) % columns == 0:
                    j += 1

    def init_players(self):
        """Δημιουργία λίστας με τους παίκτες που λαμβάνουν μέρος στο παιχνίδι"""

        if self.total_players != 1:  # στην περίπτωση που είναι ένας παίκτης ακολουθούμε άλλη διαδικασία(computer...)
            for player_number in range(1, self.total_players + 1):
                self.players.append(Player(player_number))

    def create_scoreboard(self):
        """ Δημιουργεί και τοποθετεί τα labels του σκορ του κάθε παίκτη """
        label = Label(self.score_frame, text="Scores", font="Courier 26 bold italic", bg="green").grid(row=0, column=0)
        for i, player in enumerate(self.players):
            label = Label(self.score_frame, text=f"{player.name}: {player.score}", font="Courier 16 bold", bg="green")
            label.grid(row=i + 1, column=0)

    def create_message_board(self):
        """ Τοποθετεί μηνύματα στο πάνω μέρος της οθόνης """
        label = Label(self.master, text="ABCDE", font="Courier 36 bold italic", bg="green").place(width=0.5, height=0.1)