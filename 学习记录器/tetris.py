import pygame
import random
import sys

# 初始化Pygame
pygame.init()

# 设置屏幕大小
screen = pygame.display.set_mode((300, 600))
pygame.display.set_caption('俄罗斯方块')

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (0, 255, 255), 
    (0, 0, 255), 
    (255, 165, 0), 
    (255, 255, 0), 
    (0, 255, 0), 
    (128, 0, 128), 
    (255, 0, 0)
]

# 定义方块形状
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 1], [1, 0, 0]],
]

class Tetris:
    def __init__(self):
        self.board = [[0] * 10 for _ in range(20)]
        self.current_piece = self.new_piece()
        self.piece_x, self.piece_y = 3, 0
        self.game_over = False

    def new_piece(self):
        return random.choice(SHAPES), random.choice(COLORS)

    def rotate_piece(self):
        self.current_piece = [list(row) for row in zip(*self.current_piece[0][::-1])]

    def can_move(self, dx, dy):
        shape, _ = self.current_piece
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = self.piece_x + x + dx
                    new_y = self.piece_y + y + dy
                    if new_x < 0 or new_x >= 10 or new_y >= 20 or self.board[new_y][new_x]:
                        return False
        return True

    def freeze_piece(self):
        shape, color = self.current_piece
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    self.board[self.piece_y + y][self.piece_x + x] = color
        self.clear_lines()
        self.current_piece = self.new_piece()
        self.piece_x, self.piece_y = 3, 0
        if not self.can_move(0, 0):
            self.game_over = True

    def clear_lines(self):
        self.board = [row for row in self.board if any(cell == 0 for cell in row)]
        while len(self.board) < 20:
            self.board.insert(0, [0] * 10)

    def update(self):
        if self.can_move(0, 1):
            self.piece_y += 1
        else:
            self.freeze_piece()

    def draw(self, screen):
        screen.fill(BLACK)
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, cell, (x * 30, y * 30, 30, 30))
        shape, color = self.current_piece
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, color, ((self.piece_x + x) * 30, (self.piece_y + y) * 30, 30, 30))

def main():
    clock = pygame.time.Clock()
    game = Tetris()

    while not game.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and game.can_move(-1, 0):
                    game.piece_x -= 1
                elif event.key == pygame.K_RIGHT and game.can_move(1, 0):
                    game.piece_x += 1
                elif event.key == pygame.K_DOWN:
                    game.update()
                elif event.key == pygame.K_UP:
                    game.rotate_piece()

        game.update()
        game.draw(screen)
        pygame.display.flip()
        clock.tick(10)

if __name__ == '__main__':
    main()