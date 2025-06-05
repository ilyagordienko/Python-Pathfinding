class Environment:
    """
    Represents different types of terrain or environmental types in the grid.
    Each environment has a movement cost and a flag indicating if it's an obstacle.
    """

    def __init__(self, name: str, cost: float, is_obstacle: bool, symbol: str):
        self.name = name
        self.cost = cost
        self.is_obstacle = is_obstacle
        self.symbol = symbol

    def __repr__(self):
        return (f"Environment(name='{self.name}', cost={self.cost}, is_obstacle={self.is_obstacle}, "
                f"symbol='{self.symbol}')")

    def __eq__(self, other):
        # Equality check based on name
        if not isinstance(other, Environment):
            return NotImplemented
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


# Environment types and their symbols

GROUND_SYMBOL = '.'
MUD_SYMBOL = '#'
WATER_SYMBOL = '§'
ROCK_SYMBOL = '%'
TREE_SYMBOL = 'X'

GROUND = Environment("Ground", 1.0, False, GROUND_SYMBOL)
MUD = Environment("Mud", 2.0, False, MUD_SYMBOL)
WATER = Environment("Water", 5.0, False, WATER_SYMBOL)
ROCK = Environment("Rock", float('inf'), True, ROCK_SYMBOL)
TREE = Environment("Tree", float('inf'), True, TREE_SYMBOL)

# A dictionary mapping symbols to Environment objects for easy lookup when loading maps
SYMBOL_TO_ENVIRONMENT = {
    GROUND_SYMBOL: GROUND,
    MUD_SYMBOL: MUD,
    WATER_SYMBOL: WATER,
    ROCK_SYMBOL: ROCK,
    TREE_SYMBOL: TREE
}

# A list of traversable symbols for map generation (obstacles are excluded)
TRAVERSABLE_SYMBOLS = [
    GROUND_SYMBOL,
    MUD_SYMBOL,
    WATER_SYMBOL
]
