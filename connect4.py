import sys
import numpy as np
import pygame
import math

# Board dimension
ROW_COUNT = 6
COL_COUNT = 7
SQUARE_SIZE = 100

# Colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Circle radius
RADIUS = int(SQUARE_SIZE / 2 - 5)


# Create board with default zeros
def create_board():
    return np.zeros((ROW_COUNT, COL_COUNT))


# set piece onto board (PLAYER_1 piece=1 | PLAYER_2 piece=2)
def drop_piece(g_board, c_row, c_col, piece):
    g_board[c_row][c_col] = piece


# validate columns and rows on board before dropping piece
def is_valid_location(g_board, c_col):
    return g_board[ROW_COUNT - 1][c_col] == 0


# find open row before dropping piece
def get_next_open_row(g_board, c_col):
    for i in range(ROW_COUNT - 1):
        if g_board[i][c_col] == 0:
            return i


# flip and print board
def print_board(g_board):
    print(np.flip(g_board, 0))


# find winning move after dropping piece
def wining_move(g_board, piece):
    # Check horizontal locations for win
    for c in range(COL_COUNT - 3):
        for r in range(ROW_COUNT):
            if g_board[r][c] == piece and g_board[r][c + 1] == piece and g_board[r][c + 2] == piece and g_board[r][c + 3] == piece:
                return True

    # Check Vertical locations for win
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT - 3):
            if g_board[r][c] == piece and g_board[r + 1][c] == piece and g_board[r + 2][c] == piece and g_board[r + 3][c] == piece:
                return True

    # Check positive diagonal
    for c in range(COL_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if g_board[r][c] == piece and g_board[r + 1][c + 1] == piece and g_board[r + 2][c + 2] == piece and g_board[r + 3][c + 3] == piece:
                return True

    # Check negative diagonal
    for c in range(COL_COUNT - 3):
        for r in range(3, ROW_COUNT - 3):
            if g_board[r][c] == piece and g_board[r - 1][c + 1] == piece and g_board[r - 2][c + 2] == piece and g_board[r - 3][c + 3] == piece:
                return True

    # Check negative diagonal
    for c in reversed(range(3, COL_COUNT)):
        for r in range(ROW_COUNT - 3):
            if g_board[r][c] == piece and g_board[r + 1][c - 1] == piece and g_board[r + 2][c - 2] == piece and g_board[r + 3][c - 3] == piece:
                return True


def draw_board(g_board):
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)

    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            if g_board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
            if g_board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)

            pygame.display.update()


# Board Creation
board = create_board()
game_over = False
turn = 0

pygame.init()
width = COL_COUNT * SQUARE_SIZE
height = (ROW_COUNT + 1) * SQUARE_SIZE
size = (width, height)
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()
myfont = pygame.font.SysFont("monospace", 75)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARE_SIZE / 2)), RADIUS)
            if turn == 1:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARE_SIZE / 2)), RADIUS)
            pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            print(event.pos)
            # Player1
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARE_SIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)
                    if wining_move(board, 1):
                        label = myfont.render("Player 1 wins !!!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True
            else:
                # Player2
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARE_SIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)
                    if wining_move(board, 2):
                        label = myfont.render("Player 2 wins !!!", 1, YELLOW)
                        screen.blit(label, (40, 10))
                        game_over = True

            print_board(board)
            draw_board(board)
            print("player:" + str(turn))

            turn += 1
            turn = turn % 2

            if game_over:
                pygame.time.wait(10000)
