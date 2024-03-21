import pygame
import random

class Twentyfourtyeight():
    
    def __init__(self):
        pygame.init()

        # initial set up
        self.WIDTH = 400
        self.HEIGHT = 400
        self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        pygame.display.set_caption('2048')
        self.timer = pygame.time.Clock()
        self.fps = 60
        self.font = pygame.font.Font('freesansbold.ttf', 24)

        # 2048 game color library
        self.colors = {2: (238, 228, 218),
                  4: (237, 224, 200),
                  8: (242, 177, 121),
                  16: (245, 149, 99),
                  32: (246, 124, 95),
                  64: (246, 94, 59),
                  128: (237, 207, 114),
                  256: (237, 204, 97),
                  512: (237, 200, 80),
                  1024: (237, 197, 63),
                  2048: (237, 194, 46),
                  'light text': (249, 246, 242),
                  'dark text': (119, 110, 101),
                  'other': (0, 0, 0),
                  'bg': (187, 173, 160)}

        # game variables initialize
        self.board_values = [[0 for _ in range(4)] for _ in range(4)]
        #self.board_values[0][0] = 2048
        #self.board_values[0][1] = 2048
        self.game_over = False
        self.spawn_new = True
        self.init_count = 0
        self.direction = ''

    # draw game over and restart text
    def draw_over(self):
        pygame.draw.rect(self.screen, 'black', [50, 50, 300, 100], 0, 10)
        self.game_over_text1 = self.font.render('Game Over!', True, 'white')
        self.game_over_text2 = self.font.render('Press Enter to Restart', True, 'white')
        self.screen.blit(self.game_over_text1, (130, 65))
        self.screen.blit(self.game_over_text2, (70, 105))


    # take your turn based on direction
    def take_turn(self, direc, board):
        self.merged = [[False for _ in range(4)] for _ in range(4)]
        if direc == 'UP':
            for i in range(4):
                for j in range(4):
                    self.shift = 0
                    if i > 0:
                        for q in range(i):
                            if board[q][j] == 0:
                                self.shift += 1
                        if self.shift > 0:
                            board[i - self.shift][j] = board[i][j]
                            board[i][j] = 0
                        if board[i - self.shift - 1][j] == board[i - self.shift][j] and not self.merged[i - self.shift][j] \
                                and not self.merged[i - self.shift - 1][j]:
                            board[i - self.shift - 1][j] *= 2
                            board[i - self.shift][j] = 0
                            self.merged[i - self.shift - 1][j] = True

        elif direc == 'DOWN':
            for i in range(3):
                for j in range(4):
                    self.shift = 0
                    for q in range(i + 1):
                        if board[3 - q][j] == 0:
                            self.shift += 1
                    if self.shift > 0:
                        board[2 - i + self.shift][j] = board[2 - i][j]
                        board[2 - i][j] = 0
                    if 3 - i + self.shift <= 3:
                        if board[2 - i + self.shift][j] == board[3 - i + self.shift][j] and not self.merged[3 - i + self.shift][j] \
                                and not self.merged[2 - i + self.shift][j]:
                            board[3 - i + self.shift][j] *= 2
                            board[2 - i + self.shift][j] = 0
                            self.merged[3 - i + self.shift][j] = True

        elif direc == 'LEFT':
            for i in range(4):
                for j in range(4):
                    self.shift = 0
                    for q in range(j):
                        if board[i][q] == 0:
                            self.shift += 1
                    if self.shift > 0:
                        board[i][j - self.shift] = board[i][j]
                        board[i][j] = 0
                    if board[i][j - self.shift] == board[i][j - self.shift - 1] and not self.merged[i][j - self.shift - 1] \
                            and not self.merged[i][j - self.shift]:
                        board[i][j - self.shift - 1] *= 2
                        board[i][j - self.shift] = 0
                        self.merged[i][j - self.shift - 1] = True

        elif direc == 'RIGHT':
            for i in range(4):
                for j in range(4):
                    self.shift = 0
                    for q in range(j):
                        if board[i][3 - q] == 0:
                            self.shift += 1
                    if self.shift > 0:
                        board[i][3 - j + self.shift] = board[i][3 - j]
                        board[i][3 - j] = 0
                    if 4 - j + self.shift <= 3:
                        if board[i][4 - j + self.shift] == board[i][3 - j + self.shift] and not self.merged[i][4 - j + self.shift] \
                                and not self.merged[i][3 - j + self.shift]:
                            board[i][4 - j + self.shift] *= 2
                            board[i][3 - j + self.shift] = 0
                            self.merged[i][4 - j + self.shift] = True
        return board


    # spawn in new pieces randomly when turns start
    def new_pieces(self,board):
        count = 0
        full = False
        while any(0 in row for row in board) and count < 1:
            row = random.randint(0, 3)
            col = random.randint(0, 3)
            if board[row][col] == 0:
                count += 1
                if random.randint(1, 10) == 10:
                    board[row][col] = 4
                else:
                    board[row][col] = 2
        if count < 1:
            full = True
        return board, full


    # draw background for the board
    def draw_board(self):
        pygame.draw.rect(self.screen, self.colors['bg'], [0, 0, 400, 400], 0, 10)
        pass


    # draw tiles for game
    def draw_pieces(self, board):
        for i in range(4):
            for j in range(4):
                value = board[i][j]
                if value == 0:
                    self.color = self.colors[2]  # Default color for value 0
                else:
                    if value > 8:
                        value_color = self.colors['light text']
                    else:
                        value_color = self.colors['dark text']
                    if value <= 2048:
                        self.color = self.colors[value]
                    else:
                        self.color = self.colors['other']
                pygame.draw.rect(self.screen, self.color, [j * 95 + 20, i * 95 + 20, 75, 75], 0, 5)
                if value > 0:
                    value_len = len(str(value))
                    font = pygame.font.Font('freesansbold.ttf', 48 - (5 * value_len))
                    value_text = font.render(str(value), True, value_color)
                    text_rect = value_text.get_rect(center=(j * 95 + 57, i * 95 + 57))
                    self.screen.blit(value_text, text_rect)
                    pygame.draw.rect(self.screen, 'black', [j * 95 + 20, i * 95 + 20, 75, 75], 2, 5)


    # main game loop
    def main(self):
        run = True
        while run:
            self.timer.tick(self.fps)
            self.screen.fill('gray')
            self.draw_board()
            self.draw_pieces(self.board_values)
            if self.spawn_new or self.init_count < 2:
                self.board_values, self.game_over = self.new_pieces(self.board_values)
                self.spawn_new = False
                self.init_count += 1
            if self.direction != '':
                self.board_values = self.take_turn(self.direction, self.board_values)
                self.direction = ''
                self.spawn_new = True
            if self.game_over:
                self.draw_over()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if not self.game_over:
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_UP:
                            self.direction = 'UP'
                        elif event.key == pygame.K_DOWN:
                            self.direction = 'DOWN'
                        elif event.key == pygame.K_LEFT:
                            self.direction = 'LEFT'
                        elif event.key == pygame.K_RIGHT:
                            self.direction = 'RIGHT'

                if self.game_over:
                    if event.key == pygame.K_RETURN:
                        self.board_values = [[0 for _ in range(4)] for _ in range(4)]
                        self.spawn_new = True
                        self.init_count = 0
                        self.direction = ''
                        self.game_over = False


            pygame.display.flip()
        pygame.quit()

