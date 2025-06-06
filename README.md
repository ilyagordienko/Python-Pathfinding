# Python-Pathfinding

### Running the Program

1.  **Generate a new map:**
    First, you need to create a `map.txt` file in the `maps/` directory.
    ```bash
    python generate_map_file.py
    ```
    This will create a `map.txt` (default 100x100 grid) in the `maps/` folder.

2.  **Run the pathfinding algorithm:**
    ```bash
    python main.py
    ```
    The program will load the generated map, attempt to find a path from (0,0) to (99,99) (default), display the path details, and save a full visualization to `paths/path_visualization.txt`.

### Configuration

You can modify the following settings within `main.py` and `generate_map_file.py` to customize the program's behavior:

### `main.py`
* `map_file`: Path to the input map file.
* `start_coord`: Tuple `(x, y)` for the starting cell.
* `end_coord`: Tuple `(x, y)` for the ending cell.
* `max_search_radius` (in `find_nearest_non_obstacle_cell`): Maximum radius to search for a non-obstacle start/end cell if the original is an obstacle.

### `generate_map_file.py`
* `MAP_WIDTH`, `MAP_HEIGHT`: Dimensions of the generated map.
* `ENVIRONMENT_PROBABILITIES`: A dictionary defining the probability of each environment symbol appearing on the map. Adjust these values to create maps with different terrain distributions. (Ensure probabilities sum to 1.0).
