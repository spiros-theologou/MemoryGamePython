class Player:
    """Κλάση 'Παίκτης', δέχεται έναν ακέραιο αριθμό και αποτελείται από τα γνωρίσματα name και score και τις μεθόδους str και add_score"""
    def __init__(self, player_number):
        self.player_number = player_number
        self.name = f"Player {self.player_number}"
        self.score = 0

    def __str__(self):
        return self.name

    def add_score(self, value):
        """Προσθέτει το δοθέν σκορ, στο σκορ του παίκτη"""
        self.score += value
