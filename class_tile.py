from tkinter import *

ranks = ["ace", 2, 3, 4, 5, 6, 7, 8, 9, 10, "jack", "queen", "king"]
suits = ["spades", "hearts", "clubs", "diamonds"]


class Tile(Button):
    """Κλάση tile που κληρονομεί ιδιότητες από το Button της Tk βιβλιοθήκης"""

    def __init__(self, rank, suit, is_flipped=False, **kw):
        super().__init__(**kw)
        self.rank = rank
        self.suit = suit
        self.back_image = PhotoImage(file="gui/Images/card_back.png")  # η πίσω εικόνα του tile
        self.front_image = PhotoImage(file=f"gui/Images/{self.rank}_of_{self.suit}.png")  # χρήση f-string για προσδιορισμό του path της εικόνας του tile.
        self.width = 142
        self.height = 200
        self.is_flipped = is_flipped  # γίνεται true αν ο χρήστης μπορεί να δει τη μπροστινή όψη, αλλιώς είναι false

    def __repr__(self):
        return f"({self.rank}, {self.suit})"

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def set_front_image(self, image_path):
        """ Προσδιορίζει την μπροστινή εικόνα του tile """
        front_image = PhotoImage(image_path)
        self.front_image = front_image

    def is_figure(self):
        """ Επιστρέφει true αν είναι φιγούρα, αλλιώς False"""
        if self.rank in ("jack", "queen", "king"):
            return True
        return False

    def flip(self):
        """Αλλάζει την is_flipped κατάσταση του tile"""
        self.is_flipped = not self.is_flipped

    def value(self):
        """ Επιστρέφει την αριθμητική τιμή της αξίας του tile"""
        if self.rank == "ace":
            return 1
        elif self.rank in ("jack", "queen", "king"):
            return 10
        return self.rank
