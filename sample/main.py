# import pyxel

# class App:
#     def __init__(self):
#         pyxel.init(160, 120)
#         self.x = 0
#         pyxel.run(self.update, self.draw)

#     def update(self):
#         self.x = (self.x + 1) % pyxel.width

#     def draw(self):
#         pyxel.cls(0)
#         pyxel.rect(self.x, 0, 8, 8, 9)

# App()

import pyxel
import random

SCREEN_WIDTH = 120
SCREEN_HEIGHT = 200
BLOCK_SIZE = 10
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE

SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
]


class Tetris:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Pyxel Tetris")
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_shape = None
        self.current_pos = [0, GRID_WIDTH // 2 - 2]
        self.spawn_shape()
        self.game_over = False
        self.score = 0
        pyxel.run(self.update, self.draw)

    def spawn_shape(self):
        self.current_shape = random.choice(SHAPES)
        self.current_pos = [0, GRID_WIDTH // 2 - len(self.current_shape[0]) // 2]

        if not self.is_valid_position(self.current_pos, self.current_shape):
            self.game_over = True

    def is_valid_position(self, pos, shape):
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                grid_x = pos[1] + x
                grid_y = pos[0] + y
                if cell:
                    if (
                        grid_x < 0
                        or grid_x >= GRID_WIDTH
                        or grid_y >= GRID_HEIGHT
                        or (grid_y >= 0 and self.grid[grid_y][grid_x])
                    ):
                        return False
        return True

    def lock_shape(self):
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    grid_x = self.current_pos[1] + x
                    grid_y = self.current_pos[0] + y
                    self.grid[grid_y][grid_x] = 1

        self.clear_lines()
        self.spawn_shape()

    def clear_lines(self):
        new_grid = [row for row in self.grid if any(cell == 0 for cell in row)]
        cleared_lines = GRID_HEIGHT - len(new_grid)
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(cleared_lines)] + new_grid
        self.score += cleared_lines * 100

    def rotate_shape(self):
        rotated = list(zip(*self.current_shape[::-1]))
        if self.is_valid_position(self.current_pos, rotated):
            self.current_shape = rotated

    def move_shape(self, dx, dy):
        new_pos = [self.current_pos[0] + dy, self.current_pos[1] + dx]
        if self.is_valid_position(new_pos, self.current_shape):
            self.current_pos = new_pos
        elif dy == 1:  # Lock the shape if it's moving down
            self.lock_shape()

    def update(self):
        if self.game_over:
            return

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.frame_count % 30 == 0:
            self.move_shape(0, 1)

        if pyxel.btnp(pyxel.KEY_LEFT):
            self.move_shape(-1, 0)
        if pyxel.btnp(pyxel.KEY_RIGHT):
            self.move_shape(1, 0)
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.move_shape(0, 1)
        if pyxel.btnp(pyxel.KEY_UP):
            self.rotate_shape()

    def draw(self):
        pyxel.cls(0)
        # Draw grid
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell:
                    pyxel.rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE, 11)

        # Draw current shape
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    grid_x = self.current_pos[1] + x
                    grid_y = self.current_pos[0] + y
                    pyxel.rect(
                        grid_x * BLOCK_SIZE,
                        grid_y * BLOCK_SIZE,
                        BLOCK_SIZE,
                        BLOCK_SIZE,
                        7,
                    )

        # Draw borders
        pyxel.rectb(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 8)

        # Draw score
        pyxel.text(5, 5, f"Score: {self.score}", 7)

        if self.game_over:
            pyxel.text(30, SCREEN_HEIGHT // 2 - 10, "GAME OVER", 8)


Tetris()









