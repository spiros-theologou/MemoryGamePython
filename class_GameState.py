class GameState:
    """Κλάση που περιέχει τις πληροφορίες για να συνεχίσουμε ένα παιχνίδι από ένα συγκεκριμένο σημείο"""
    def __init__(self, current_player, player_index, tiles_info: list, players_list: list, open_tiles, total_tiles, difficulty):
        self.current_player = current_player
        self.player_index = player_index
        self.tiles_info = tiles_info
        self.players_list = players_list
        self.open_tiles = open_tiles
        self.total_tiles = total_tiles
        self.difficulty = difficulty
