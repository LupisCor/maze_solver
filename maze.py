from cell import Cell
import random
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
            win = None,
            seed = None,
    ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        if seed:
            random.seed(seed)
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0,0)
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

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.01)
    
    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_cols -1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            next_cell_list = []

            # Left
            if i > 0 and not self._cells[i-1][j].visited:
                next_cell_list.append((i-1, j))
            # Right
            if i < self._num_cols - 1 and not self._cells[i+1][j].visited:
                    next_cell_list.append((i+1, j))
            # Up
            if j > 0 and not self._cells[i][j-1].visited:
                next_cell_list.append((i, j-1))
            # Down
            if j < self._num_rows - 1 and not self._cells[i][j+1].visited:
                next_cell_list.append((i, j+1))

            if len(next_cell_list) == 0:
                self._draw_cell(i, j)
                return
            
            direction = random.choice(next_cell_list)

            # Right
            if direction[0] == i+1:
                self._cells[i][j].has_right_wall = False
                self._cells[i+1][j].has_left_wall = False
            # Left
            if direction[0] == i-1:
                self._cells[i][j].has_left_wall = False
                self._cells[i-1][j].has_right_wall = False
            # Up
            if direction[1] == j-1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j-1].has_bottom_wall = False
            # Down
            if direction[1] == j+1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j+1].has_top_wall = False
            
            self._break_walls_r(direction[0], direction[1])
    
    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False
    
    def solve(self):
        if self._solver_r(0, 0):
            print("Maze Solved!")
            return True
    
    def _solver_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        if self._cells[i][j] == self._cells[self._num_cols - 1][self._num_rows - 1]:
            return True
        
        # Left
        if i > 0 and not self._cells[i][j].has_left_wall and not self._cells[i-1][j].visited:
            self._cells[i][j].draw_move(self._cells[i-1][j])
            if self._solver_r(i-1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i-1][j], True)
        # Right
        if i < self._num_cols - 1 and not self._cells[i][j].has_right_wall and not self._cells[i+1][j].visited:
            self._cells[i][j].draw_move(self._cells[i+1][j])
            if self._solver_r(i+1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i+1][j], True)
        # Up
        if j > 0 and not self._cells[i][j].has_top_wall and not self._cells[i][j-1].visited:
            self._cells[i][j].draw_move(self._cells[i][j-1])
            if self._solver_r(i, j-1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j-1], True)
        # Down
        if j < self._num_rows - 1 and not self._cells[i][j].has_bottom_wall and not self._cells[i][j+1].visited:
            self._cells[i][j].draw_move(self._cells[i][j+1])
            if self._solver_r(i, j+1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j+1], True)
        return False
