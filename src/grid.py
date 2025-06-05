import collections
from typing import List, Dict, Tuple, Optional, Set

from src.environment import Environment


class Cell:
    def __init__(self, x: int, y: int, environment_type: Environment):
        self.x = x
        self.y = y
        self.environment_type = environment_type
        self.g_score = float('inf')
        self.h_score = 0.0
        self.f_score = float('inf')
        self.parent: Optional['Cell'] = None

    def __lt__(self, other):
        return self.f_score < other.f_score

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return isinstance(other, Cell) and self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x},{self.y})"

    @property
    def coords(self) -> Tuple[int, int]:
        return self.x, self.y


class Grid:
    def __init__(self, map_data: List[List[str]], symbol_to_environment: Dict[str, Environment]):
        if not map_data or not map_data[0]:
            raise ValueError("Map data cannot be empty.")

        self.height = len(map_data)
        self.width = len(map_data[0])
        self.cells: List[List[Cell]] = []
        self.symbol_to_environment = symbol_to_environment

        self.start_node: Optional[Cell] = None
        self.end_node: Optional[Cell] = None

        for r in range(self.height):
            row_cells = []
            for c in range(self.width):
                symbol = map_data[r][c]
                environment = self.symbol_to_environment.get(symbol)
                if not environment:
                    raise ValueError(f"Unknown environment symbol '{symbol}' at ({r},{c}). "
                                     f"Check map file and SYMBOL_TO_ENVIRONMENT mapping.")
                cell = Cell(c, r, environment)
                row_cells.append(cell)
            self.cells.append(row_cells)

        self.start_node = self.get_cell(0, 0)
        self.end_node = self.get_cell(self.width - 1, self.height - 1)

    def get_cell(self, x: int, y: int) -> Optional[Cell]:
        """Returns the Cell object at the given (x, y) coordinates, or None if out of bounds."""
        if 0 <= y < self.height and 0 <= x < self.width:
            return self.cells[y][x]
        return None

    def get_neighbors(self, cell: Cell) -> List[Cell]:
        """Returns a list of valid, non-obstacle neighbors for a given cell."""
        neighbors = []
        movements = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dx, dy in movements:
            new_x, new_y = cell.x + dx, cell.y + dy
            neighbor_cell = self.get_cell(new_x, new_y)
            if neighbor_cell and not neighbor_cell.environment_type.is_obstacle:
                neighbors.append(neighbor_cell)
        return neighbors

    def print_grid(self) -> None:
        """Prints the full grid to the console."""
        for r in range(self.height):
            row_str = ""
            for c in range(self.width):
                cell = self.get_cell(c, r)
                if cell:
                    row_str += cell.environment_type.symbol
                else:
                    row_str += '?'
            print(row_str)

    def print_sample(self, sample_size: int = 25) -> None:
        """Prints a sample (top-left) section of the grid to the console."""
        print(f"--- Sample Grid ({sample_size}x{sample_size}) ---")
        for r in range(min(sample_size, self.height)):
            row_str = ""
            for c in range(min(sample_size, self.width)):
                cell = self.get_cell(c, r)
                if cell:
                    row_str += cell.environment_type.symbol
                else:
                    row_str += '?'
            print(row_str)
        if self.width > sample_size or self.height > sample_size:
            print("...")

    def _get_display_symbol(self, cell: Cell, path_coords_set: Set[Tuple[int, int]]) -> str:
        """Helper to get the symbol for display, including path overlay (S, E, ■)."""
        if self.start_node and (cell.x, cell.y) == self.start_node.coords:
            return 'S'
        elif self.end_node and (cell.x, cell.y) == self.end_node.coords:
            return 'E'
        elif (cell.x, cell.y) in path_coords_set:
            return '■'
        else:
            return cell.environment_type.symbol

    def render_grid_with_path(self, path: List['Cell']) -> str:
        """
        Generates a multi-line string representation of the grid with the path highlighted.
        'S' for start, 'E' for end, '*' for path, and environment symbols otherwise.
        """
        if not self.start_node or not self.end_node:
            raise ValueError("Start and end nodes must be set on the grid for path rendering.")

        path_coords_set = {(cell.x, cell.y) for cell in path}
        display_lines = []

        for r in range(self.height):
            row_str = ""
            for c in range(self.width):
                cell = self.get_cell(c, r)
                if cell:
                    row_str += self._get_display_symbol(cell, path_coords_set)
                else:
                    row_str += '?'
            display_lines.append(row_str)
        return "\n".join(display_lines)

    def print_grid_with_path(self, path: List['Cell'], sample_size: Optional[int] = None) -> None:
        """
        Prints the grid with the path highlighted to the console.
        Can print a sample if sample_size is provided.
        """
        full_grid_str = self.render_grid_with_path(path)
        lines = full_grid_str.splitlines()

        if sample_size is not None and (self.width > sample_size or self.height > sample_size):
            print_width = sample_size
            print_height = sample_size
            for r in range(min(print_height, len(lines))):
                print(lines[r][:print_width])
            print("...")
        else:
            print(full_grid_str)


# --- find_nearest_non_obstacle_cell (standalone function) ---
# Corrected E125: Indented the return type on a new line
def find_nearest_non_obstacle_cell(grid: Grid, start_x: int, start_y: int, max_search_radius: int = 5) -> \
        Optional[Tuple[int, int]]:
    """
    Finds the nearest non-obstacle cell to a given (x,y) coordinate using BFS.
    Returns (x, y) tuple of the non-obstacle cell, or None if not found within radius.
    """
    queue = collections.deque([(start_x, start_y, 0)])
    visited = {(start_x, start_y)}

    while queue:
        curr_x, curr_y, dist = queue.popleft()

        if dist > max_search_radius:
            continue

        cell = grid.get_cell(curr_x, curr_y)
        if cell and not cell.environment_type.is_obstacle:
            return curr_x, curr_y

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor_x, neighbor_y = curr_x + dx, curr_y + dy
            if (0 <= neighbor_x < grid.width and
                    0 <= neighbor_y < grid.height and
                    (neighbor_x, neighbor_y) not in visited):
                visited.add((neighbor_x, neighbor_y))
                queue.append((neighbor_x, neighbor_y, dist + 1))

    return None
