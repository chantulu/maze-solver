import random
from cell import Cell
from graphics import Point, Window
import time


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win: Window = None,
        seed=None,
    ) -> None:
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []
        self._create_cells()
        self._break_entrance_and_exit()
        self.seed = seed
        if seed is not None:
            self.seed = random.seed(seed)
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)

        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self, stime=0.02):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(stime)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[-1][-1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r_bad(self, i, j):
        current = (i, j)
        self._cells[i][j].visited = True
        while True:
            to_visit = []
            # Check for unvisited neighbors
            neighbors = [
                (i, j - 1),  # left
                (i, j + 1),  # right
                (i + 1, j),  # down
                (i - 1, j),  # up
            ]
            for x, y in neighbors:
                if (
                    0 <= x < len(self._cells)
                    and 0 <= y < len(self._cells[0])
                    and not self._cells[x][y].visited
                ):
                    to_visit.append((x, y))
            if len(to_visit) == 0:
                self._draw_cell(i, j)
                return
            next_cell = random.choice(to_visit)
            x, y = next_cell

            if y == j - 1:  # left
                self._cells[current[0]][current[1]].has_left_wall = False
                self._cells[x][y].has_right_wall = False
            elif y == j + 1:  # right
                self._cells[current[0]][current[1]].has_right_wall = False
                self._cells[x][y].has_left_wall = False
            elif x == i + 1:  # down
                self._cells[current[0]][current[1]].has_bottom_wall = False
                self._cells[x][y].has_top_wall = False
            elif x == i - 1:  # up
                self._cells[current[0]][current[1]].has_top_wall = False
                self._cells[x][y].has_bottom_wall = False
            self._break_walls_r(next_cell[0], next_cell[1])

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            next_index_list = []

            # determine which cell(s) to visit next
            # left
            if i > 0 and not self._cells[i - 1][j].visited:
                next_index_list.append((i - 1, j))
            # right
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                next_index_list.append((i + 1, j))
            # up
            if j > 0 and not self._cells[i][j - 1].visited:
                next_index_list.append((i, j - 1))
            # down
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                next_index_list.append((i, j + 1))

            # if there is nowhere to go from here
            # just break out
            if len(next_index_list) == 0:
                self._draw_cell(i, j)
                return

            # randomly choose the next direction to go
            direction_index = random.randrange(len(next_index_list))
            next_index = next_index_list[direction_index]

            # knock out walls between this cell and the next cell(s)
            # right
            if next_index[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False
            # left
            if next_index[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False
            # down
            if next_index[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False
            # up
            if next_index[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False

            # recursively visit the next cell
            self._break_walls_r(next_index[0], next_index[1])

    def solve(self):
        return self.solve_r(0, 0)

    def solve_r(self, i, j):
        c = (i, j)
        self._animate(0.5)
        self._cells[c[0]][c[1]].visited = True
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True
        neighbors = [
            (i, j - 1),  # left
            (i, j + 1),  # right
            (i + 1, j),  # down
            (i - 1, j),  # up
        ]
        to_visit = []
        for x, y in neighbors:
            if (
                0 <= x < len(self._cells)
                and 0 <= y < len(self._cells[0])
                and not self._cells[x][y].visited
            ):
                to_visit.append((x, y))
        print(f"Neighbors to visit from {c}: {to_visit}")
        worked = False
        for d in to_visit:
            nxt = self._cells[d[0]][d[1]]
            print(f"Checking direction: {d}")
            if (
                d[0] == i - 1
                and d[1] == j
                and not self._cells[c[0]][c[1]].has_left_wall
                and not nxt.has_right_wall
            ):
                self._cells[c[0]][c[1]].draw_move(nxt)
                print("left")
                if self.solve_r(d[0], d[1]):
                    return True
                else:
                    self._cells[c[0]][c[1]].draw_move(nxt, True)

            if (
                d[0] == i + 1
                and d[1] == j  # right
                and not self._cells[c[0]][c[1]].has_right_wall
                and not nxt.has_left_wall
            ):
                self._cells[c[0]][c[1]].draw_move(nxt)
                print("right")
                if self.solve_r(d[0], d[1]):
                    return True
                else:
                    self._cells[c[0]][c[1]].draw_move(nxt, True)

            if (
                d[0] == i
                and d[1] == j + 1  # down
                and not self._cells[c[0]][c[1]].has_bottom_wall
                and not nxt.has_top_wall
            ):
                self._cells[c[0]][c[1]].draw_move(nxt)
                print("down")
                if self.solve_r(d[0], d[1]):
                    worked = True
                    return True
                else:
                    self._cells[c[0]][c[1]].draw_move(nxt, True)
            if (
                d[0] == i
                and d[1] == j - 1  # up
                and not self._cells[c[0]][c[1]].has_top_wall
                and not nxt.has_bottom_wall
            ):  # up
                self._cells[c[0]][c[1]].draw_move(nxt)
                print("up")
                if self.solve_r(d[0], d[1]):
                    worked = True
                    return True
                else:
                    self._cells[c[0]][c[1]].draw_move(nxt, True)
        if worked == False:
            return False

    def _reset_cells_visited(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False
