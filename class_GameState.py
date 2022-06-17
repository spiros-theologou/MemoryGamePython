class GameState:
    """Κλάση που περιέχει τις πληροφορίες για να συνεχίσουμε ένα παιχνίδι από ένα συγκεκριμένο σημείο"""

    def __init__(self, player_index, tiles_info: list, players_list: list, open_tiles, total_tiles, difficulty, computer_score=None, computer_history=None):
        self.player_index = player_index
        self.tiles_info = tiles_info
        self.players_list = players_list
        self.open_tiles = open_tiles
        self.total_tiles = total_tiles
        self.difficulty = difficulty
        self.computer_score = computer_score
        self.computer_history = computer_history
