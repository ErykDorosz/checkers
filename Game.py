import pygame
from Data import Data
from Board import Board


class Game:
    def __init__(self, win):
        self._init()                    # Inicjalizacja zmiennych wyświetlanych w oknie gry
        self.win = win                  # Przypisanie okna

    ####################################
    # Metoda rysująca całą plansze     #
    # przeznaczona do jej aktualizacji #
    ####################################

    def update(self, row, col):
        self.board.draw(self.win, row, col, self.turn)
        if self.board.check_if_piece(row, col) and self.turn == self.board.get_piece(row, col).color:
            self.draw_valid_moves(self.valid_moves)
        self.display_description()
        pygame.display.update()

    #########################################################
    # Metoda inicjalizująca zmienne wyświetlane w oknie gry #
    #########################################################

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = Data.WHITE
        self.valid_moves = {}

    #########################################
    # Metoda zwracająca zwycięzcę rozgrywki #
    #########################################

    def winner(self):
        return self.board.winner()

    ###########################
    # Metoda restartująca grę #
    ###########################

    def reset(self):
        self._init()

    #######################################
    # Metoda obsługująca kliknięcie myszą #
    # przez gracza                        #
    #######################################

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            self.longest_move()
            return True

        return False

    ####################################################
    # Metoda wykonująca ruch pionem, usuwa zbite piony #
    ####################################################

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    #############################################
    # Metoda rysująca zielone kólko oznaczające #
    # możliwość wykonania ruchu na dane pole    #
    #############################################

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(
                self.win, Data.GREEN, (col * Data.SQUARE_SIZE + Data.SQUARE_SIZE // 2,
                                       row * Data.SQUARE_SIZE + Data.SQUARE_SIZE // 2), 15)

    ###########################################
    # Metoda zmieniająca kolej na przeciwnika #
    ###########################################

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == Data.RED:
            self.turn = Data.WHITE
        else:
            self.turn = Data.RED

    #########################################
    # Metoda tworząca komunikat informujący #
    # o aktualnym stanie rozgrywki          #
    #########################################

    def display_description(self):
        font = pygame.font.Font('freesansbold.ttf', 32)
        self.win.blit(font.render('RUCH WYKONUJĄ: ', True, Data.SKYBLUE), (Data.WIDTH - 775, Data.HEIGHT - 85))
        if self.turn == Data.WHITE:
            self.win.blit(font.render('BIAŁE', True, Data.WHITE), (Data.WIDTH - 460, Data.HEIGHT - 85))
        else:
            self.win.blit(font.render('CZERWONE', True, Data.RED), (Data.WIDTH - 460, Data.HEIGHT - 85))
        self.win.blit(
            font.render(
                'ZBITE PIONY PRZECIWNIKA: ' + str(12 - self.board.red_left), True,
                Data.SKYBLUE
                ), (Data.WIDTH - 775, Data.HEIGHT - 45)
            )

    #############################################
    # Metoda usuwająca ruchy krótsze od maximum #
    #############################################

    def longest_move(self):
        self.max = 0
        for piecelist in self.valid_moves.values():
            if piecelist != 0:
                piecelist = list(dict.fromkeys(piecelist))

                piecelist = list(set(piecelist))

                if piecelist != 0:
                    piecelist = list(set(piecelist))
                    if len(piecelist) > self.max:
                        self.max = len(piecelist)

        longest_move = self.valid_moves.copy()

        for key, piecelist in longest_move.items():
            if not piecelist:
                if self.max != 0:
                    del self.valid_moves[key]
            else:
                if self.max != len(set(piecelist)):
                    del self.valid_moves[key]

    #############################################
    # Metoda tworząca komunikat informujący     #
    # o aktualnym stanie rozgrywki, przyjmująca #
    # wiadomość do wyświetlenia oraz jej        #
    # współrzędne jako parametry                #
    #############################################

    def display_text(self, text, x, y):
        font = pygame.font.Font('freesansbold.ttf', 32)
        self.win.blit(
            font.render(text, True, Data.SKYBLUE), (x, y)
            )
        pygame.display.update()
