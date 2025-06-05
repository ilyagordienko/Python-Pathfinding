import os
import random
from typing import List

# Import symbols from environment.py (CORRIDOR_SYMBOL removed)
from src.environment import (
    GROUND_SYMBOL, WATER_SYMBOL, MUD_SYMBOL, ROCK_SYMBOL, TREE_SYMBOL)

# --- Configuration ---
MAP_WIDTH = 100
MAP_HEIGHT = 100
output_dir = "maps"
output_filename = os.path.join(output_dir, "map.txt")

# Define the probabilities for each environment type (sum should be 1.0)
ENVIRONMENT_PROBABILITIES = {
    GROUND_SYMBOL: 0.5,
    WATER_SYMBOL: 0.2,
    MUD_SYMBOL: 0.2,
    ROCK_SYMBOL: 0.05,
    TREE_SYMBOL: 0.05
}

# Ensure probabilities sum to 1.0 (or close enough due to float precision)
if not (0.99 <= sum(ENVIRONMENT_PROBABILITIES.values()) <= 1.01):
    raise ValueError("Sum of ENVIRONMENT_PROBABILITIES must be approximately 1.0")


def create_random_map_data(width: int, height: int) -> List[List[str]]:
    """
    Creates a 2D list representing the map with random environment types
    based on defined probabilities.
    """
    map_data = []
    env_symbols = list(ENVIRONMENT_PROBABILITIES.keys())
    probabilities = list(ENVIRONMENT_PROBABILITIES.values())

    for _ in range(height):
        row = random.choices(env_symbols, weights=probabilities, k=width)
        map_data.append(row)
    return map_data


# The add_corridor_to_map function has been completely removed as requested.

def save_map_to_file(map_data: List[List[str]], filepath: str):
    """
    Saves the generated map data to a text file.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:  # Keep UTF-8 encoding for '■' and '§'
        for row in map_data:
            f.write("".join(row) + "\n")


def main():
    print(f"Generating a {MAP_WIDTH}x{MAP_HEIGHT} map...")

    # Generate random map data
    map_data = create_random_map_data(MAP_WIDTH, MAP_HEIGHT)

    # Save the map to file
    save_map_to_file(map_data, output_filename)
    print(f"Map saved to '{output_filename}'")
    print("Now run main.py to find a shortest path on the grid.")


if __name__ == "__main__":
    main()
