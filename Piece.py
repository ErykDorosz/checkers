import pygame

from Data import Data


class Piece:

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = Data.SQUARE_SIZE * self.col + Data.SQUARE_SIZE // 2
        self.y = Data.SQUARE_SIZE * self.row + Data.SQUARE_SIZE // 2

    ##########################################
    # Metoda nadająca atrubut damy dla piona #
    ##########################################

    def make_king(self):
        self.king = True

    #########################
    # Metoda rysująca piona #
    #########################

    def draw(self, win):
        radius = Data.SQUARE_SIZE // 2 - Data.PADDING
        if self.king:
            pygame.draw.circle(win, Data.GOLD, (self.x, self.y), radius + 5 + Data.OUTLINE, 0)

        pygame.draw.circle(win, self.color, (self.x, self.y), radius + Data.OUTLINE)

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):
        return str(self.color)
