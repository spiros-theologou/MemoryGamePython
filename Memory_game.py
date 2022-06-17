from class_tile import *
from random import shuffle, choice  # χρειάζεται για το ανακάτεμα των φύλλων
from class_player import Player  # η κλάση που ορίζει τον παίκτη με τα βασικά του γνωρίσματα
from time import sleep  # για να μην ανανεώνεται κατευθείαν η σελίδα πριν προλάβει ο παίκτης να δει τα φύλλα που ανοίξανε
from class_GameState import *  # για την δημιουργία του GameState object που θα χρησιμοποιηθεί για την αποθύκευση
from class_Computer import Computer  # για τη δημιουργία του AI Παίκτη
import pickle  # για την αποθήκευση


class NewGame:
    """Κλάση New Game, δημιουργεί το board και την υλοποίηση του νέου παιχνιδιού,
     δεδομένων της δυσκολίας και του αριθμού των παιχτών"""

    def __init__(self, master, difficulty, total_players):
        self.master = master
        self.difficulty = difficulty
        self.total_players = total_players

        # Αρχικοποίηση του υπολογιστή σε None(αλλάζει αν ο παίκτης είναι ένας στη μέθοδο init_players)
        self.computer = None

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

        # Δημιουργία του frame που θα τοποθετηθεί η λεζάντα των μηνυμάτων παιχνιδιού(ποιος παίζει, αν έχουμε match η όχι κλπ...)
        self.message_frame = Frame(master, bg="green")
        self.message_frame.columnconfigure(index=0, weight=1)
        self.message_frame.rowconfigure(index=0, weight=1)
        self.message_frame.place(relx=0.5, rely=0.5, anchor="n")

        # Αρχικοποίηση του αριθμού των "γυρισμένων" tiles ανά γύρο(click_count - θα βοηθήσει στο να προσδιορίσουμε πότε τελειώνει ο γύρος για έναν παίκτη)
        # της λίστας με τα επιλεγμένα tiles ανά γύρο
        # και του index του παίκτη που παίζει
        self.current_player_index = 0  # το index του τρέχοντος παίκτη
        self.current_player = self.players[0]  # ο τρέχων παίκτης
        self.click_count = 0  # μεταβλητή που αποθηκεύει των αριθμό των κλικαρισμένων tiles ανά γύρο
        self.clicked_tiles = []  # λίστα στην οποία θα αποθηκεύονται προσωρινά τα ανοιγμένα tiles του γύρου

        # Αρχικοποίηση του αριθμού των "ανοιχτών" και των "κλειστών" tiles
        self.open_tiles = 0
        self.total_tiles = len(self.tiles)

        # Δημιουργία και τοποθέτηση του scoreboard
        self.create_scoreboard()

        # Δημιουργία και τοποθέτηση του message_board
        self.create_message_board()

        # Δημιουργία αντικειμένου GameState για την αποθήκευση του παιχνιδιού
        self.current_state = GameState(self.current_player_index, self.tiles, self.players, self.open_tiles, self.total_tiles, self.difficulty)

        # Εκκινούμε τον γύρο με τον υπολογιστή αν υπάρχει
        if self.current_player.name == "Computer":  # αν ο τρέχων παίκτης έιναι ο υπολογιστής, καλούμε τη μέθοδο που υλοποιεί το γύρο του
            self.computer_turn()


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
        if not tile.is_flipped:
            if self.computer:
                self.computer.memorize_tile(tile)


            self.click_count += 1  # μετρητής των click για αυτόν το γύρο
            self.flip(tile)
            self.master.update()  # ανανέωση του master για εμφάνιση των ανοιχτών tiles.
            self.clicked_tiles.append(tile)
            self.check_king_queen()  # έλεγχος για το αν έχουμε ζέυγος king-queen
            # συγκρίνουμε τα tiles αν είναι 2 κλικαρισμένα
            if self.click_count == 2:
                self.compare_tiles(self.clicked_tiles)
                self.change_player()  # αλλαγή τρέχοντος παίκτη
                self.clicked_tiles.clear()  # καθαρισμός της λίστας των κλικαρισμένων tiles
                self.click_count = 0
                self.message.configure(text=f"{self.current_player} ", fg="black")
                if self.current_player != self.computer:
                    self.save_game()  # αποθηκεύει την κατάσταση του παιχνιδιού στο τέλος κάθε 2ου γύρου
                end = self.check_game_end()  # έλεγχος για τη λήξη του παιχνιδιού
                if not end:
                    if isinstance(self.current_player, Computer):
                        self.computer_turn()
        else:
            pass

    def compare_tiles(self, tile_list):
        """Συγκρίνει τα tiles της λίστας, ανανεώνει κατάλληλα το μήνυμα και το scoreboard"""

        if len(tile_list) == 2:  # στην περίπτωση που δεν έχει ανοίξει ο συνδυασμός Ρήγας-ντάμα
            if tile_list[0].rank != tile_list[1].rank:  # αν δεν ταιριάζουν, τα γυρνάμε ανάποδα
                self.message.configure(text="NO MATCH!", fg="red")
                self.message.update()
                sleep(0.7)
                for t in tile_list:
                    self.flip(t)
            else:
                self.message.configure(text="MATCH!", fg="blue")
                if self.computer:
                    self.computer.remove_tiles(self.clicked_tiles)
                self.message.update()
                sleep(0.7)
                self.current_player.add_score(tile_list[0].value())
                self.update_scoreboard()
                self.open_tiles += 2

        else:  # στην περίπτωση που έχουμε Ρήγα-ντάμα- 3ο φύλλο
            kings_count = 0  # μετρητής για του kings
            queens_count = 0  # μετρητής για τις queens

            # απαρίθμηση των kings και queens
            for tile in tile_list:
                if tile.rank == "king":
                    kings_count += 1
                elif tile.rank == "queen":
                    queens_count += 1
            # διαχωρισμός περιπτώσεων
            if kings_count == 2:
                self.message.configure(text="MATCH!", fg="blue")
                self.computer.remove_tiles(self.clicked_tiles)
                self.message.update()
                sleep(0.7)
                self.current_player.add_score(10)
                self.update_scoreboard()
                self.open_tiles += 2
                for tile in tile_list:
                    if tile.rank == "queen":
                        self.flip(tile)

            elif queens_count == 2:
                self.message.configure(text="MATCH!", fg="blue")
                try:
                    self.computer.remove_tiles(self.clicked_tiles)
                except AttributeError:
                    pass
                self.message.update()
                sleep(0.7)
                self.current_player.add_score(10)
                self.update_scoreboard()
                self.open_tiles += 2
                for tile in tile_list:
                    if tile.rank == "king":
                        self.flip(tile)

            else:
                self.message.configure(text="NO MATCH!", fg="red")
                self.message.update()
                sleep(0.7)
                for tile in tile_list:
                    self.flip(tile)

    def flip(self, tile):
        """Συνάρτηση που 'γυρίζει' ένα tile"""
        if not tile.is_flipped:
            # αν το tile είναι face down, το γυρίζει και αφαιρεί τη λειτουργικότητα
            tile.image = tile.front_image
            tile.flip()
            tile.configure(image=tile.image)
            tile.configure(command=0)
        else:
            if tile.is_flipped:
                tile.image = tile.back_image
                tile.flip()
                tile.configure(image=tile.image)
                tile.configure(command=lambda t=tile: self.button_click(t))

    def add_tile_functionality(self):
        """ Προσθήκη λειτουργικότητας στα tiles, αλλάζοντας την εικόνα που φαίνεται στο tile που κλικάρεται"""
        for tile in self.tiles:
            tile.configure(command=lambda t=tile: self.button_click(t))

    def create_board(self):
        """Δημιουργεί το board, ανάλογα με τη δυσκολία"""

        # Εύκολο
        if self.difficulty == "easy":
            columns = 4
            print("Initializing Easy Board")
            # Τοποθέτηση των tiles
            j = 0
            for k, tile in enumerate(self.tiles):
                tile.image = tile.back_image
                tile.configure(image=tile.image)
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
                tile.image = tile.back_image
                tile.configure(image=tile.image)
                tile.grid(row=j, column=k % columns, padx=10, pady=10)
                if (k + 1) % columns == 0:
                    j += 1

        # Δύσκολο
        if self.difficulty == "hard":
            columns = 13
            print("Initializing Hard Board")
            # Τοποθέτηση των tiles
            j = 0
            for k, tile in enumerate(self.tiles):
                tile.image = tile.back_image
                tile.configure(image=tile.image)
                tile.grid(row=j, column=k % columns, padx=6, pady=6)
                if (k + 1) % columns == 0:
                    j += 1

    def init_players(self):
        """Δημιουργία λίστας με τους παίκτες που λαμβάνουν μέρος στο παιχνίδι"""

        # MULTIPLAYER
        if self.total_players != 1:
            for player_number in range(1, self.total_players + 1):
                self.players.append(Player(player_number))
        # SINGLE PLAYER
        else:
            self.computer = Computer()
            self.players.append(self.computer)
            self.players.append(Player(1))

    def create_scoreboard(self):
        """ Δημιουργεί και τοποθετεί τα labels του σκορ του κάθε παίκτη,
         επίσης δημιουργεί ένα dictionary με το label για το score του κάθε παίκτη(key=player, value=label)"""
        self.player_scores = dict()
        self.scoreboard = Label(self.score_frame, text="Scores", font="Courier 26 bold italic", bg="green")
        self.scoreboard.grid(row=0, column=0)
        for i, player in enumerate(self.players):
            label = Label(self.score_frame, text=f"{player.name}: {player.score}", font="Courier 16 bold", bg="green")
            self.player_scores[player] = label
            label.grid(row=i + 1, column=0)

    def create_message_board(self):
        """ Τοποθετεί μηνύματα στο πάνω μέρος της οθόνης """
        self.message = Label(self.master, text=f"{self.current_player}", font="Courier 36 bold italic", bg="green")
        self.message.pack(pady=50)

    def update_scoreboard(self):
        """Ανaνεώνει το scoreboard"""
        for player, label in self.player_scores.items():
            label.configure(text=f"{player.name}: {player.score}")

    def change_player(self):
        """Προχωράει στον επόμενο παίκτη"""
        if self.clicked_tiles[0].rank == self.clicked_tiles[1].rank == "jack":  # αν έχουμε ανοίξει βαλέδες ξαναπαίζει ο ίδιος πάικτης
            return None
        # Έλεγχος για τον αριθμό των ρηγάδων(μπορεί να είναι και λίστα με 3 στοιχεία)
        kings = 0  # αρχικοποιεί τον αριθμό των ρηγάδων
        for t in self.clicked_tiles:
            if t.rank == "king":
                kings += 1
        if kings == 2:  # αν έχουμε ανοίξει 2 ρηγάδες ο επόμενος παίκτης χάνει τη σειρά του
            self.current_player_index += 2
            self.current_player_index = self.current_player_index % len(self.players)
            self.current_player = self.players[self.current_player_index]
        else:
            self.current_player_index += 1
            self.current_player_index = self.current_player_index % len(self.players)
            self.current_player = self.players[self.current_player_index]

    def check_king_queen(self):
        """Ελέγχει αν τα 2 πρώτα φύλλα που ανοίχτηκαν είναι king and queen και εκτελεί τις ανάλογες διαδικασίες"""
        try:
            if {self.clicked_tiles[0].rank, self.clicked_tiles[1].rank} == {"king", "queen"} and len(self.clicked_tiles) <= 2:
                self.message.configure(text="Ρήγας και Ντάμα, επίλεξε τρίτη κάρτα!")
                self.message.update()
                self.click_count -= 1  # μειώνουμε το click count, ώστε να μην αλλάξει ο γύρος
                if self.current_player == self.computer:
                    print("Computer chooses a third card")
                    self.choose_third_card()
        except IndexError:
            pass

    def save_game(self):
        """Καλείται στο τέλος κάθε γύρου. Ενημερώνει το GameState και το αποθηκεύει, κάνοντας overwrite το προηγούμενο"""

        self.current_state.tiles_info = [(tile.rank, tile.suit, tile.is_flipped) for tile in self.tiles]  # αποθηκεύει την κατάσταση του κάθε tile σε μια λίστα, ώστε να μπορούμε να το κάνουμε recreate
        self.current_state.open_tiles = self.open_tiles
        self.current_state.player_index = self.current_player_index
        self.current_state.players_list = self.players[:]

        # Αν υπάρχει ΑΙ παιρνάμε το score του και μια λίστα με τα index των tiles που βρίσκονται στο ιστορικό του
        if self.computer:
            self.current_state.players_list.pop(0)
            self.current_state.computer_score = self.computer.score
            self.current_state.computer_history_indexes = [self.tiles.index(tile) for tile in self.computer.history]

        with open("saved_game_data.pickle", "wb") as outfile:
            pickle.dump(self.current_state, outfile)

    def check_game_end(self):
        """Ελέγχει αν το παιχνίδι έχει τελειώσει συγκρίνοντας τον αριθμό των ανοιγμένων tiles
        με τον αριθμό των συνολικών, στη συνέχεια ανακοινώνει τον νικητή βρίσκοντας το μέγιστο score"""
        end = False
        if self.open_tiles == self.total_tiles:
            end = True
            max_score = max([player.score for player in self.players])  # βρίσκουμε το μέγιστο σκορ
            winners = []  # λίστα με τους νικητές
            for player in self.players:
                if player.score == max_score:
                    winners.append(player)

            self.message.configure(text="GAME OVER!", fg="yellow")
            self.message.update()
            sleep(0.7)
            if len(winners) == 1:
                self.message.configure(text=f"\n\nΝικητής είναι ο: {winners[0]}, με {winners[0].score} πόντους!\n\n\nΕυχαριστούμε που παίξατε!")
                self.board_frame.destroy()
                self.message.update()
            else:
                winners_names = ""
                for winner in winners:
                    winners_names += f"{winner.name}, "

                self.board_frame.destroy()
                self.message.configure(text=f"\n\nΤο παιχνίδι είναι ισοπαλία \nμεταξύ των {winners_names}\nμε τελικό σκορ {max_score} πόντους!\n\n\nΕυχαριστούμε που παίξατε!")
                self.message.update()
        return end

    def computer_turn(self):
        """Οι δράσεις που κάνει ο υπολογιστής στον γύρο του"""
        self.master.config(cursor="none")
        self.master.update()
        sleep(0.4)
        first_tile = None

        def select_random_closed_tile(a_tile):
            """ Επιστρέφει ένα τυχαίο κλειστό tile"""
            found = False
            while not found:
                t = choice(self.tiles)
                if not t.is_flipped and t.suit != a_tile.suit:
                    return t

        # Έλεγχος για την ύπαρξη κοινών tiles στο ιστορικό καρτών με χρήση διπλής επανάληψης
        # για την αποφυγή διπλών συγκρίσεων πχ. το history[0] με το history [2] και μετά το history[2] με το history[0]
        # αν βρεθεί ισότητα ως προς το rank γυρίζουμε τις 2 κάρτες που ταιριάζουν και τις αφαιρούμε από το ιστορικό καρτών
        # προσάπτονται στον υπολογιστή οι ανάλογοι πόντοι και τερματίζεται ο γύρος του.
        if self.computer.history:
            try:
                for i in range(len(self.computer.history)):
                    for j in range(i + 1, len(self.computer.history)):
                        if self.computer.history[i].rank == self.computer.history[j].rank:
                            self.button_click(self.computer.history[i])
                            sleep(0.7)
                            self.button_click(self.computer.history[j])
                            self.computer.remove_tiles(self.clicked_tiles)
                            self.master.config(cursor="")
                            return None
            except IndexError:
                pass

            # προχωράμε στο ενδεχόμενο όπου δεν βρέθηκαν κάρτες που ταιριάζουν

            # βρίσκουμε την πρώτη διαθέσιμη κλειστή κάρτα
            for tile in self.tiles:
                if not tile.is_flipped:
                    first_tile = tile
                    break

            self.button_click(first_tile)
            sleep(0.7)
            # ελέγχουμε αν υπάρχει στο ιστορικό καρτών
            for card in self.computer.history:
                if (first_tile.rank == card.rank) and (first_tile.suit != card.suit):
                    self.button_click(card)
                    sleep(0.7)
                    self.computer.remove_tiles(self.clicked_tiles)
                    break
            else:
                second_tile = select_random_closed_tile(first_tile)
                self.button_click(second_tile)
        # αν ΔΕΝ υπάρχει ιστορικό καρτών
        else:
            # βρίσκουμε την πρώτη διαθέσιμη κάρτα
            for tile in self.tiles:
                if not tile.is_flipped:
                    first_tile = tile
                    self.button_click(first_tile)
                    sleep(0.7)
                    break
            # επιλέγουμε μια τυχαία κλειστή κάρτα
            second_tile = select_random_closed_tile(first_tile)
            self.button_click(second_tile)
            sleep(0.7)

        self.master.config(cursor="")
        self.master.update()

    def choose_third_card(self):
        """Ο υπολογιστής επιλέγει 3η κάρτα στην περίπτωση του K-Q combo"""
        sleep(0.7)
        for tile in self.computer.history:
            if (tile.rank == "king" or tile.rank == "queen") and (not tile.is_flipped) and (tile not in self.clicked_tiles):
                self.button_click(tile)
                return None

        found = False
        while not found:
            t = choice(self.tiles)
            if not t.is_flipped and t not in self.clicked_tiles:
                found = True
            self.button_click(t)