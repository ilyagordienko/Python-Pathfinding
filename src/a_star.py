import heapq
from typing import List, Optional

# Import Cell and Grid classes from the grid
from .grid import Cell, Grid


class AStarPathfinder:

    # A* pathfinding algorithm to find the shortest path

    def __init__(self, grid: Grid):
        self.grid = grid

    @staticmethod
    def _heuristic(cell_a: Cell, cell_b: Cell) -> float:

        # Calculates the distance between two cells and cost of movement.

        return abs(cell_a.x - cell_b.x) + abs(cell_a.y - cell_b.y)

    def find_path(self, start_cell: Cell, end_cell: Cell) -> Optional[List[Cell]]:
        """
        Finds the shortest path from start_cell to end_cell.
        Args:
            start_cell: The starting Cell object.
            end_cell: The target Cell object.
        Returns:
            A list of Cell objects representing the path from start to end,
            or None if no path is found.
        """
        start_cell.g_score = 0
        start_cell.f_score = self._heuristic(start_cell, end_cell)
        start_cell.parent = None

        open_set = [(start_cell.f_score, start_cell)]

        closed_set = set()

        while open_set:
            current_f_score, current_cell = heapq.heappop(open_set)

            if current_cell == end_cell:
                return self._reconstruct_path(current_cell)

            if current_cell in closed_set:
                continue

            closed_set.add(current_cell)

            for neighbor in self.grid.get_neighbors(current_cell):
                if neighbor.environment_type.is_obstacle:
                    continue

                if neighbor in closed_set:
                    continue

                tentative_g_score = current_cell.g_score + neighbor.environment_type.cost

                # If this path to neighbor's cell is better than any previous one
                if tentative_g_score < neighbor.g_score:
                    neighbor.parent = current_cell
                    neighbor.g_score = tentative_g_score
                    neighbor.f_score = neighbor.g_score + self._heuristic(neighbor, end_cell)

                    heapq.heappush(open_set, (neighbor.f_score, neighbor))

        return None  # No path found

    @staticmethod
    def _reconstruct_path(current_cell: Cell) -> List[Cell]:
        """
        Reconstructs the path from the end_cell back to the start_cell
        using the parent pointers stored directly in the Cell objects.
        """
        path = []
        while current_cell:
            path.append(current_cell)
            current_cell = current_cell.parent
        return path[::-1]  # Reverse the path to get it from start to end
