import os
from collections import Counter
from typing import List

from src.a_star import AStarPathfinder
from src.environment import SYMBOL_TO_ENVIRONMENT, GROUND_SYMBOL, MUD_SYMBOL, WATER_SYMBOL, ROCK_SYMBOL, TREE_SYMBOL
from src.grid import Grid, find_nearest_non_obstacle_cell
from src.visualize_grid_map import generate_grid_image_with_images


def load_map_from_file(filepath: str) -> List[List[str]]:
    """Loads map data from a txt file."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Map file not found at '{filepath}'")

    map_data = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            stripped_line = line.strip()
            if stripped_line:
                map_data.append(list(stripped_line))
    return map_data


# Path Output Configuration
output_path_dir = "paths"
output_path_filename = os.path.join(output_path_dir, "path_visualization.txt")


def save_path_to_file(grid_representation: str, filepath: str):
    """Saves the grid with the path to a txt file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(grid_representation)
    print(f"\nGrid with path visualization saved to '{filepath}'")


def main():
    print("Pathfinding...")

    #  1. Configuration
    map_file_absolute_path = r"C:\Programming\Python\navigation_grid\maps\map.txt"
    start_coord = (0, 0)
    end_coord = (99, 99)

    image_mapping = {
        GROUND_SYMBOL: 'ground10x10.png',
        MUD_SYMBOL: 'mud10x10.png',
        WATER_SYMBOL: 'water10x10.png',
        ROCK_SYMBOL: 'rock10x10.png',
        TREE_SYMBOL: 'tree10x10.png'
    }

    #  2. Load Map and Create Grid
    try:
        full_map_filepath = map_file_absolute_path

        map_data = load_map_from_file(full_map_filepath)
        grid = Grid(map_data, SYMBOL_TO_ENVIRONMENT)
        print(f"Map loaded successfully from '{full_map_filepath}'. Dimensions: {grid.width}x{grid.height}\n")
    except (FileNotFoundError, ValueError) as e:
        print(f"Error loading map: {e}")
        print("Please ensure 'generate_map_file.py' has been run to create 'map.txt'.")
        return

    #  3. Display Grid (console)
    print("Initial Grid:")
    grid.print_grid()

    #  4. Validate and Adjust Start/End Points if on Obstacles
    start_x, start_y = start_coord
    end_x, end_y = end_coord

    start_cell_original = grid.get_cell(start_x, start_y)
    end_cell_original = grid.get_cell(end_x, end_y)

    if not start_cell_original:
        print(f"Error: Start coordinates ({start_x},{start_y}) are out of map bounds.")
        return
    if not end_cell_original:
        print(f"Error: End coordinates ({end_x},{end_y}) are out of map bounds.")
        return

    # Adjust start point if it's an obstacle
    if start_cell_original.environment_type.is_obstacle:
        print(
            f"Warning: Start cell ({start_x},{start_y}) is an obstacle ({start_cell_original.environment_type.name}).")
        adjusted_start_coords = find_nearest_non_obstacle_cell(grid, start_x, start_y, max_search_radius=5)
        if adjusted_start_coords:
            start_x, start_y = adjusted_start_coords
            start_cell = grid.get_cell(start_x, start_y)
            print(
                f"Adjusted start to nearest non-obstacle: ({start_x},{start_y}) ({start_cell.environment_type.name}).")
        else:
            print("Error: Could not find a reachable non-obstacle start cell nearby. Exiting.")
            return
    else:
        start_cell = start_cell_original

    # Adjust end point if it's an obstacle
    if end_cell_original.environment_type.is_obstacle:
        print(f"Warning: End cell ({end_x},{end_y}) is an obstacle ({end_cell_original.environment_type.name}).")
        adjusted_end_coords = find_nearest_non_obstacle_cell(grid, end_x, end_y, max_search_radius=5)
        if adjusted_end_coords:
            end_x, end_y = adjusted_end_coords
            end_cell = grid.get_cell(end_x, end_y)
            print(f"Adjusted end to nearest non-obstacle: ({end_x},{end_y}) ({end_cell.environment_type.name}).")
        else:
            print("Error: Could not find a reachable non-obstacle end cell nearby. Exiting.")
            return
    else:
        end_cell = end_cell_original

    print(f"Attempting to find path from Start: {start_cell} to End: {end_cell}\n")

    #  5. Find a Path
    pathfinder = AStarPathfinder(grid)
    path = pathfinder.find_path(start_cell, end_cell)

    #  6. Display Results
    if path:
        print(f"Path found! Total cost: {path[-1].g_score:.2f}")
        print("Path coordinates:")
        if len(path) > 2:
            print(f"  {path[0]} -> ... -> {path[-1]}")
            print(f"  Total steps: {len(path)}")
        else:
            print("  " + " -> ".join(str(cell) for cell in path))

        # Count and display cell types used in the path
        path_cell_type_counts = Counter()
        for cell in path:
            path_cell_type_counts[cell.environment_type.name] += 1

        print("\nThe cells through which the path passed:")
        for name, count in path_cell_type_counts.most_common():
            print(f"  {count} {name} cells were used in the path.")
        print("-" * 30)

        print("\nGrid with Path (console view):")
        grid.print_grid_with_path(path, sample_size=None)

        full_path_grid_string = grid.render_grid_with_path(path)

        base_output_dir = os.path.dirname(map_file_absolute_path)
        full_output_path_filepath = os.path.join(os.path.dirname(base_output_dir), output_path_filename)
        save_path_to_file(full_path_grid_string, full_output_path_filepath)

        print("\nGenerating visual map images...")

        image_output_base_dir = os.path.dirname(base_output_dir)
        generate_grid_image_with_images(grid, image_mapping,
                                        output_filename=os.path.join(image_output_base_dir, 'plain_grid_map.png'))
        generate_grid_image_with_images(grid, image_mapping, path=path,
                                        output_filename=os.path.join(image_output_base_dir, 'grid_with_path_map.png'))

    else:
        print("No path found between the start and end cells.")
        print("This could be due to obstacles, disconnected areas, or unreachable target.")
        print("Check environment definitions, map content, or start/end points.")


if __name__ == "__main__":
    main()
