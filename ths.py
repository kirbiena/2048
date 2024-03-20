import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 4
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 Game")

# Set up fonts
font = pygame.font.Font(None, 36)

# Helper functions
def draw_tile(x, y, value):
    if value > 0:
        tile_color = get_tile_color(value)
        text_color = BLACK if value < 8 else WHITE
        pygame.draw.rect(screen, tile_color, (x*GRID_WIDTH, y*GRID_HEIGHT, GRID_WIDTH, GRID_HEIGHT))
        text_surface = font.render(str(value), True, text_color)
        text_rect = text_surface.get_rect(center=(x*GRID_WIDTH + GRID_WIDTH//2, y*GRID_HEIGHT + GRID_HEIGHT//2))
        screen.blit(text_surface, text_rect)

def get_tile_color(value):
    colors = {2: (238, 228, 218), 4: (237, 224, 200), 8: (242, 177, 119), 16: (245, 149, 99), 32: (246, 124, 95),
              64: (246, 94, 59), 128: (237, 207, 114), 256: (237, 204, 97), 512: (237, 200, 80), 1024: (237, 197, 63),
              2048: (237, 194, 46)}
    return colors.get(value, (205, 193, 180))

def new_tile(board):
    while True:
        x = random.randrange(GRID_SIZE)
        y = random.randrange(GRID_SIZE)
        if board[y][x] == 0:
            board[y][x] = 2 if random.random() < 0.9 else 4
            break

def slide(row, reverse=False):
    slide_row = [tile for tile in row if tile != 0]
    if reverse:
        slide_row = slide_row[::-1]
    slide_row += [0] * (GRID_SIZE - len(slide_row))
    return slide_row

def merge(row, reverse=False):
    merged_row = slide(row, reverse)
    for i in range(len(merged_row) - 1):
        if (reverse and merged_row[i] == merged_row[i+1]) or (not reverse and merged_row[i] == merged_row[i+1]):
            merged_row[i] *= 2
            merged_row[i+1] = 0
    merged_row = slide(merged_row, reverse)
    return tuple(merged_row)  # Convert the list back to a tuple

def move(board, direction):
    if direction == "up":
        board[:] = list(zip(*board[::-1]))
        for index, row in enumerate(board):
            board[index] = list(merge(row))
        board[:] = list(zip(*board[::-1]))
    elif direction == "down":
        board[:] = list(zip(*board[::-1]))
        for index, row in enumerate(board):
            board[index] = list(merge(row, True))
        board[:] = list(zip(*board[::-1]))
    elif direction == "left":
        for index, row in enumerate(board):
            board[index] = list(merge(row))
    elif direction == "right":
        for index, row in enumerate(board):
            board[index] = list(merge(row, True))

def check_game_over(board):
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if board[y][x] == 0:
                return False
            if x < GRID_SIZE - 1 and board[y][x] == board[y][x+1]:
                return False
            if y < GRID_SIZE - 1 and board[y][x] == board[y+1][x]:
                return False
    return True

# Initialize game board
board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
new_tile(board)
new_tile(board)

# Game loop
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move(board, "up")
            elif event.key == pygame.K_DOWN:
                move(board, "down")
            elif event.key == pygame.K_LEFT:
                move(board, "left")
            elif event.key == pygame.K_RIGHT:
                move(board, "right")
            if not check_game_over(board):
                new_tile(board)

    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            draw_tile(x, y, board[y][x])

    pygame.display.flip()