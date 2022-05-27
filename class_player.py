class Player:
    """Κλάση 'Παίκτης', καθορίζει τα γνωρίσματα ενός παίχτη δεδομένου του αριθμού του.(player 1, player 2 ...)"""
    def __init__(self, player_number):
        self.player_number = player_number
        self.name = f"Player {self.player_number}"
        self.score = 0
        self.plays = False  # γίνεται True αν παίζει σε αυτόν το γύρο

    def __str__(self):
        return self.name

    def add_score(self, value):
        self.score += value

    def turn(self):
        """ Αλλάζει το value του self.plays όταν ξεκινάει και τελειώνει ο γύρος του παίκτη """
        self.plays = not self.plays
