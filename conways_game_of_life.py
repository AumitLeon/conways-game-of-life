import os
import random
import time
from collections import deque
from enum import Enum


class Pattern(Enum):
    GLIDER = 1


class ConwaysGameOfLife:
    def __init__(
        self,
        rows: int,
        cols: int,
        simulation_speed: float = 0.5,
        seed_live_start: int | None = None,
        pattern: Pattern | None = None,
    ):
        self.rows = rows
        self.cols = cols
        self.grid = [["." for col in range(cols)] for rows in range(rows)]
        self.next_grid = [["." for col in range(cols)] for rows in range(rows)]
        self.simulation_speed = simulation_speed
        self.live_cells = set()
        self.next_live_cells = set()
        self.iteration_queue = deque()
        self.pattern = pattern
        self.default_seed_live_start = 20
        self.seed_live_start = (
            seed_live_start
            if seed_live_start
            else random.choice(range(self.default_seed_live_start))
        )
        if not self.pattern:
            self._init_state()
        else:
            print("init the pattern")
            self._init_pattern()

    def _init_state(self):
        for i in range(self.seed_live_start):
            random_row = random.choice(range(self.rows))
            random_col = random.choice(range(self.cols))
            while ((random_row, random_col)) in self.live_cells:
                random_row = random.choice(range(self.rows))
                random_col = random.choice(range(self.cols))
            self.grid[random_row][random_col] = "O"
            self.live_cells.add((random_row, random_col))

    def _init_pattern(self):
        if self.pattern == Pattern.GLIDER:
            if self.rows < 50 or self.cols < 50:
                raise ValueError("Grid too small for glider pattern.")
            # Center is [15][15]
            self.grid[14][15] = "O"
            self.grid[15][16] = "O"
            self.grid[16][14] = "O"
            self.grid[16][15] = "O"
            self.grid[16][16] = "O"
            self.live_cells.add((14, 15))
            self.live_cells.add((15, 16))
            self.live_cells.add((16, 14))
            self.live_cells.add((16, 15))
            self.live_cells.add((16, 16))

    def draw_grid(self, iteration: int):
        # 'nt' is for Windows, 'posix' is for Linux/macOS
        os.system("cls" if os.name == "nt" else "clear")
        for row in self.grid:
            print("".join(row))

        print(f"Iteration: {iteration} with {len(self.live_cells)} live cells")
        print()

    def get_possible_positions(self, row, col):
        return [
            (row + 1, col),
            (row - 1, col),
            (row, col + 1),
            (row, col - 1),
            # Diagonals
            (row + 1, col + 1),
            (row + 1, col - 1),
            (row - 1, col - 1),
            (row - 1, col + 1),
        ]

    def get_valid_positions(self, row, col):
        return [
            pos
            for pos in self.get_possible_positions(row, col)
            if self.is_valid_position(pos[0], pos[1])
        ]

    def is_valid_position(self, row, col):
        if 0 > row or row >= self.rows or 0 > col or col >= self.cols:
            return False
        return True

    def evaluate_cell(self, row, col) -> str:
        is_alive = True if self.grid[row][col] == "O" else False
        alive_neighbor_count = 0
        dead_neighbor_count = 0
        for position in self.get_valid_positions(row, col):
            neighbor_row, neighbor_col = position
            if (neighbor_row, neighbor_col) in self.live_cells:
                alive_neighbor_count += 1
            else:
                dead_neighbor_count += 1

        if is_alive and (alive_neighbor_count in (2, 3)):
            self.next_live_cells.add((row, col))
            return "O"
        elif is_alive:
            # self.next_live_cells.remove((row, col))
            return "."

        if not is_alive and (alive_neighbor_count == 3):
            self.next_live_cells.add((row, col))
            return "O"
        else:
            return "."

    def simulate(self):
        iteration = 0
        print(f"Initialized with {len(self.live_cells)} cells")
        self.draw_grid(-1)
        while True:
            for row_idx, row in enumerate(self.grid):
                for col_idx, col in enumerate(row):
                    self.next_grid[row_idx][col_idx] = self.evaluate_cell(
                        row_idx, col_idx
                    )
            self.grid = self.next_grid
            self.next_grid = [
                ["." for col in range(self.cols)] for rows in range(self.rows)
            ]
            self.live_cells = self.next_live_cells
            self.next_live_cells = set()
            self.draw_grid(iteration)
            time.sleep(self.simulation_speed)
            iteration += 1


# game = ConwaysGameOfLife(rows=50, cols=50, seed_live_start=300)
game = ConwaysGameOfLife(rows=50, cols=50, pattern=Pattern.GLIDER)
game.simulate()
