from class_player import Player


class Computer(Player):
    """ Είναι ο υπολογιστής που έχει αντίπαλο ο παίκτης στο single player. """
    def __init__(self, player_number=0):
        super().__init__(player_number)
        self.name = "Computer"
        self.history = []

    def memorize_tile(self, tile):
        """Προσθέτει το κλικαρισμένο tile στη μνήμη και
        αφαιρεί το 1ο στοιχείο, αν είναι πάνω από 5 tiles αποθηκευμένα"""

        if tile not in self.history:
            self.history.append(tile)

        if len(self.history) > 5:
            self.history.pop(0)

    def remove_tiles(self, tile_list):
        for tile in tile_list:
            try:
                self.history.remove(tile)
            except ValueError:
                pass
