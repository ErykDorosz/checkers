import pygame
from Data import Data
from Piece import Piece

WIN = pygame.display.set_mode((Data.WIDTH, Data.HEIGHT))
pygame.display.set_caption('Checkers')


class Board:
    def __init__(self):
        self.board = []                         # Plansza (przy inicjalizacji jest pusta)
        self.red_left = self.white_left = 12    # Ilosc pionow jest na planszy
        self.red_kings = self.white_kings = 0   # Ilosc damek
        self.create_board()                     # Tworzenie planszy
        #self.create_custom_board()            # Custom board - plansza przeznaczona do testów


    ###########################
    # Metoda rysująca plansze #
    ###########################

    def draw_squares(self, win):
        win.fill(Data.BLACK)
        for row in range(Data.ROWS):
            for col in range(row % 2, Data.COLS, 2):
                pygame.draw.rect(
                    win, Data.GREY, (
                        row * Data.SQUARE_SIZE, col * Data.SQUARE_SIZE, Data.SQUARE_SIZE, Data.SQUARE_SIZE)
                    )

    #########################################
    # Metoda podświetlająca wybranego piona #
    #########################################

    def light_selected(self, row, col):
        piece = self.board[row][col]
        pygame.draw.rect(
            WIN, Data.GREEN,
            (col * Data.SQUARE_SIZE, row * Data.SQUARE_SIZE, Data.SQUARE_SIZE, Data.SQUARE_SIZE)
            )
        pygame.draw.rect(
            WIN, Data.BLACK,
            (col * Data.SQUARE_SIZE + 2, row * Data.SQUARE_SIZE + 2, Data.SQUARE_SIZE - 4,
             Data.SQUARE_SIZE - 4)
            )
        radius = Data.SQUARE_SIZE // 2 - Data.PADDING
        if piece.king:
            pygame.draw.circle(WIN, Data.GOLD, (piece.x, piece.y), radius + 5 + Data.OUTLINE, 0)

        pygame.draw.circle(WIN, piece.color, (piece.x, piece.y), radius + Data.OUTLINE)

    #################################################################
    # Metoda przemieszczjąca piona po wykonaniu drugiego kliknięcia #
    # Używana w klasie Game.py                                      #
    #################################################################

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        if row == Data.ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == Data.WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1

    #############################################################
    # Metoda zwracająca piona z planszy przyjmującą współrzędne #
    # row - wiersze, col - kolumny                              #
    #############################################################

    def get_piece(self, row, col):
        return self.board[row][col]

    ###########################
    # Metoda tworząca plansze #
    ###########################

    def create_board(self):
        for row in range(Data.ROWS):
            self.board.append([])
            for col in range(Data.COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, Data.RED))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, Data.WHITE))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    ###############################################
    # Metoda sprawdzająca, czy pod wybranym polem #
    # znajduje się pion                           #
    ###############################################

    def check_if_piece(self, row, col):
        if 7 >= row >= 0 and 7 >= col >= 0:
            if self.board[row][col] != 0:
                return True

        return False

    ###############################################
    # Metoda sprawdzająca, czy pod wybranym polem #
    # znajduje się pion przeciwnika               #
    ###############################################

    def check_if_enemy_piece(self, row, col, color):
        if self.check_if_piece(row, col):
            if color == Data.WHITE and self.get_piece(row, col).color == Data.RED:
                return True
            elif color == Data.RED and self.get_piece(row, col).color == Data.WHITE:
                return True

        return False

    ####################################
    # Metoda rysująca piony na planszy #
    ####################################

    def draw(self, win, r, c, turn):
        self.draw_squares(win)
        for row in range(Data.ROWS):
            for col in range(Data.COLS):
                if row == r and col == c and self.check_if_piece(row, col) and turn == self.get_piece(row, col).color:
                    self.light_selected(r, c)
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    #############################################
    # Metoda usuwająca piony z listy pieces     #
    # Używana w klasie Game.py w metodzie _move #
    #############################################

    def remove(self, pieces):
        if pieces:
            for piece in pieces:
                if piece:
                    self.board[piece.row][piece.col] = 0

            red_pieces = 0
            white_pieces = 0
            for row in range(Data.ROWS):
                for col in range(Data.COLS):
                    if self.board[row][col] != 0:
                        if self.get_piece(row, col).color == Data.RED:
                            red_pieces += 1
                        elif self.get_piece(row, col).color == Data.WHITE:
                            white_pieces += 1

            self.white_left = white_pieces
            self.red_left = red_pieces

    #########################################################
    # Metoda zwracająca zwycięzcę rozgrywki (lub jego brak) #
    #########################################################

    def winner(self):
        if self.red_left <= 0:
            return Data.WHITE
        elif self.white_left <= 0:
            return Data.RED

        return None

    ####################################################
    # Metoda zwracająca liste możliwych ruchów zarówno #
    # dla piona jak i dla damki                        #
    ####################################################

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row
        if piece.king:                                                                                       # RUCHY DLA DAM
            moves.update(self._capture_moves_left_king(row - 1, -1, -1, piece.color, left, Data.TOPLEFT))    # Po lewej przekątnej w górę
            moves.update(self._capture_moves_right_king(row - 1, -1, -1, piece.color, right, Data.TOPRIGHT)) # Po prawej przekątnej w górę
            moves.update(self._capture_moves_left_king(row + 1, 8, 1, piece.color, left, Data.BOTLEFT))      # Po lewej przekątnej w dół
            moves.update(self._capture_moves_right_king(row + 1, 8, 1, piece.color, right, Data.BOTRIGHT))   # Po prawej przekątnej w dół

        elif piece.color == Data.WHITE:                                                                      # RUCHY DLA PIONÓW:
            moves.update(self._capture_moves_left(row - 1, max(row - 3, -1), -1, piece.color, left))         # Po lewej przekątnej do przodu
            moves.update(self._capture_moves_right(row - 1, max(row - 3, -1), -1, piece.color, right))       # Po prawej przekątnej do przodu
        elif piece.color == Data.RED:
            moves.update(self._capture_moves_left(row + 1, min(row + 3, Data.ROWS), 1, piece.color, left))   # Po lewej przekątnej do tyłu
            moves.update(self._capture_moves_right(row + 1, min(row + 3, Data.ROWS), 1, piece.color, right)) # Po prawej przekątnej do tyłu

        return moves

    ##################################################
    # Metoda wykorzystująca rekurencję, aby stworzyć #
    # tablicę ruchów po lewej przekątnej             #
    ##################################################

    def _capture_moves_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    last += skipped
                    moves[(r, left)] = last
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, -1) ##########
                    else:
                        row = min(r + 3, Data.ROWS)
                    moves.update(self._capture_moves_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._capture_moves_right(r + step, row, step, color, left + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
            left -= 1

        return moves

    ##################################################
    # Metoda wykorzystująca rekurencję, aby stworzyć #
    # tablicę ruchów po prawej przekątnej            #
    ##################################################

    def _capture_moves_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= Data.COLS:
                break

            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    last += skipped
                    moves[(r, right)] = last
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, -1) #### -1 -> 0
                    else:
                        row = min(r + 3, Data.ROWS)
                    moves.update(self._capture_moves_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._capture_moves_right(r + step, row, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
            right += 1

        return moves

    ##################################################
    # Metoda wykorzystująca rekurencję, aby stworzyć #
    # tablicę ruchów po lewej przekątnej dla damki   #
    ##################################################

    def _capture_moves_left_king(self, start, stop, step, color, left, dir, skipped=[]):
        moves = {}
        last = []
        lastlist = skipped.copy()
        captured = False
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current == 0:
                if len(last) != 0:
                    lastlist += last
                    moves[(r, left)] = lastlist
                    captured = True
                if not captured and not skipped:
                    moves[(r, left)] = current

                if captured:
                    if self.steps_top_left(r, left, color) and dir != Data.BOTRIGHT:
                        moves.update(self._capture_moves_left_king(r + step, -1, step, color, left - 1, Data.TOPLEFT,
                                                                   skipped=lastlist))

                    if self.steps_top_right(r, left, color) and dir != Data.BOTLEFT:
                        moves.update(self._capture_moves_right_king(r + step, -1, step, color, left + 1, Data.TOPRIGHT,
                                                                    skipped=lastlist))

                    if self.steps_bottom_left(r, left, color) and dir != Data.TOPRIGHT:
                        moves.update(self._capture_moves_left_king(r - step, 8, -step, color, left - 1, Data.BOTLEFT,
                                                                   skipped=lastlist))

                    if self.steps_bottom_right(r, left, color) and dir != Data.TOPLEFT:
                        moves.update(self._capture_moves_right_king(r - step, 8, -step, color, left + 1, Data.BOTRIGHT,
                                                                    skipped=lastlist))

            elif current.color == color:
                break
            else:
                last = [current]
            left -= 1

        return moves

    ##################################################
    # Metoda wykorzystująca rekurencję, aby stworzyć #
    # tablicę ruchów po prawej przekątnej dla damki  #
    ##################################################

    def _capture_moves_right_king(self, start, stop, step, color, right, dir, skipped=[]):
        moves = {}
        last = []
        lastlist = skipped.copy()
        captured = False
        for r in range(start, stop, step):
            if right >= Data.COLS:
                break

            current = self.board[r][right]
            if current == 0:
                if len(last) != 0:
                    lastlist += last
                    moves[(r, right)] = lastlist
                    captured = True
                if not captured and not skipped:
                    moves[(r, right)] = current

                if captured:
                    if self.steps_top_left(r, right, color) and dir != Data.BOTRIGHT:
                        moves.update(
                            self._capture_moves_left_king(
                                r + step, -1, step, color, right - 1, Data.TOPLEFT, skipped=lastlist
                                )
                            )

                    if self.steps_top_right(r, right, color) and dir != Data.BOTLEFT:
                        moves.update(
                            self._capture_moves_right_king(
                                r + step, -1, step, color, right + 1, Data.TOPRIGHT, skipped=lastlist
                                )
                            )

                    if self.steps_bottom_left(r, right, color) and dir != Data.TOPRIGHT:
                        moves.update(
                            self._capture_moves_left_king(
                                r - step, 8, -step, color, right - 1, Data.BOTLEFT, skipped=lastlist
                                )
                            )

                    if self.steps_bottom_right(r, right, color) and dir != Data.TOPLEFT:
                        moves.update(
                            self._capture_moves_right_king(
                                r - step, 8, -step, color, right + 1, Data.BOTRIGHT, skipped=lastlist
                                )
                            )

            elif current.color == color:
                break
            else:
                last = [current]
            right += 1

        return moves

    ###############################################################
    # Metoda sprawdzająca, czy na danej przekątnej istnieje bicie #
    # Wykorzystywana w metodach z biciem damy                     #
    ###############################################################

    def steps_top_left(self, row, col, color):
        ytop = row
        xleft = col

        lastx = -10
        lasty = -10
        while ytop >= 0 and xleft >= 0:

            if self.check_if_piece(ytop, xleft) and not self.check_if_enemy_piece(ytop, xleft, color):
                break

            if self.check_if_piece(ytop, xleft) and self.check_if_enemy_piece(ytop, xleft, color):
                lasty = ytop
                lastx = xleft

            if ytop - lasty == -1 and xleft - lastx == -1:
                if not self.check_if_piece(ytop, xleft):
                    return True
                else:
                    return False
            ytop -= 1
            xleft -= 1

        return False

    ###############################################################
    # Metoda sprawdzająca, czy na danej przekątnej istnieje bicie #
    # Wykorzystywana w metodach z biciem damy                     #
    ###############################################################

    def steps_top_right(self, row, col, color):
        ytop = row
        xright = col
        lastx = -10
        lasty = -10
        while ytop >= 0 and xright <= 7:

            if self.check_if_piece(ytop, xright) and not self.check_if_enemy_piece(ytop, xright, color):
                break

            if self.check_if_piece(ytop, xright) and self.check_if_enemy_piece(ytop, xright, color):
                lasty = ytop
                lastx = xright

            if ytop - lasty == -1 and xright - lastx == 1:
                if not self.check_if_piece(ytop, xright):
                    return True
                else:
                    return False

            ytop -= 1
            xright += 1

        return False

    ###############################################################
    # Metoda sprawdzająca, czy na danej przekątnej istnieje bicie #
    # Wykorzystywana w metodach z biciem damy                     #
    ###############################################################

    def steps_bottom_left(self, row, col, color):
        ybot = row
        xleft = col

        lastx = -10
        lasty = -10
        while ybot <= 7 and xleft >= 0:

            if self.check_if_piece(ybot, xleft) and not self.check_if_enemy_piece(ybot, xleft, color):
                break

            if self.check_if_piece(ybot, xleft) and self.check_if_enemy_piece(ybot, xleft, color):
                lasty = ybot
                lastx = xleft

            if ybot - lasty == 1 and xleft - lastx == -1:
                if not self.check_if_piece(ybot, xleft):
                    return True
                else:
                    return False

            ybot += 1
            xleft -= 1

        return False

    ###############################################################
    # Metoda sprawdzająca, czy na danej przekątnej istnieje bicie #
    # Wykorzystywana w metodach z biciem damy                     #
    ###############################################################

    def steps_bottom_right(self, row, col, color):
        ybot = row
        xright = col
        lastx = -10
        lasty = -10
        while ybot <= 7 and xright <= 7:

            if self.check_if_piece(ybot, xright) and not self.check_if_enemy_piece(ybot, xright, color):
                break

            if self.check_if_piece(ybot, xright) and self.check_if_enemy_piece(ybot, xright, color):
                lasty = ybot
                lastx = xright

            if ybot - lasty == 1 and xright - lastx == 1:
                if not self.check_if_piece(ybot, xright):
                    return True
                else:
                    return False

            ybot += 1
            xright += 1

        return False

    ###############################################################
    # Metoda sprawdzająca czy wybrane pole jest w obszare planszy #
    ###############################################################

    def check_if_valid_squre(self, row, col):
        if 7 >= row >= 0 and 7 >= col >= 0:
            return True

        return False

    ############################################################
    # Metoda zamieniająca naszą planszę w tablicę intów gdzie: #
    # 0 - puste pole                                           #
    # 1 - biały pion                                           #
    # 2 - czerwony pion                                        #
    # 3 - biała dama                                           #
    # 4 - czerwona dama                                        #
    ############################################################

    def change_to_send_board(self):
        send_board = []
        for row in range(Data.ROWS):
            send_board.append([])
            for col in range(Data.COLS):
                send_board[row].append(0)

        for row in range(Data.ROWS):
            for col in range(Data.COLS):
                if self.board[row][col] != 0:
                    if self.get_piece(row, col).color == Data.RED:
                        if self.get_piece(row, col).king:
                            send_board[row][col] = 4
                        else:
                            send_board[row][col] = 2
                    elif self.get_piece(row, col).color == Data.WHITE:
                        if self.get_piece(row, col).king:
                            send_board[row][col] = 3
                        else:
                            send_board[row][col] = 1

        return send_board

    ################################################################
    # Metoda zamieniająca tablicę intów na naszą plansze z pionami #
    ################################################################

    def change_to_board(self, send_board):
        for row in range(Data.ROWS):
            for col in range(Data.COLS):
                self.board[row][col] = 0
        red_pieces = 0
        white_pieces = 0
        for row in range(Data.ROWS):
            for col in range(Data.COLS):
                if send_board[row][col] != 0:

                    if send_board[row][col] == 2:
                        red_pieces += 1
                        self.board[row][col] = (Piece(row, col, Data.RED))
                    elif send_board[row][col] == 1:
                        white_pieces += 1
                        self.board[row][col] = (Piece(row, col, Data.WHITE))
                    elif send_board[row][col] == 3:
                        white_pieces += 1
                        king = Piece(row, col, Data.WHITE)
                        king.king = True
                        self.board[row][col] = king
                    elif send_board[row][col] == 4:
                        red_pieces += 1
                        king = Piece(row, col, Data.RED)
                        king.king = True
                        self.board[row][col] = king

        self.red_left = red_pieces
        self.white_left = white_pieces
        return self.board


    ######################################
    # Pomocnicza metoda tworząca planszę #
    # ze specjalnym ustawieniem pionów,  #
    # wykorzystywana tylko do testów     #
    ######################################

    def create_custom_board(self):
        for row in range(Data.ROWS):
            self.board.append([])
            for col in range(Data.COLS):
                self.board[row].append(0)

        # self.board[2][1] = (Piece(2, 1, Data.RED))
        # self.board[4][3] = (Piece(4, 3, Data.RED))
        # self.board[6][5] = (Piece(6, 5, Data.RED))
        #
        # self.board[7][6] = (Piece(7, 6, Data.WHITE))
        ##########
        # self.board[2][1] = (Piece(2, 1, Data.WHITE))
        # self.board[4][3] = (Piece(4, 3, Data.WHITE))
        # self.board[6][5] = (Piece(6, 5, Data.WHITE))

        # self.board[6][1] = (Piece(6, 1, Data.WHITE))
        # self.board[2][5] = (Piece(2, 5, Data.WHITE))
        self.board[6][3] = (Piece(6, 3, Data.WHITE))
        self.board[4][5] = (Piece(4, 5, Data.WHITE))

        # self.board[1][0] = (Piece(1, 0, Data.RED))
        # self.board[1][6] = (Piece(1, 6, Data.RED))
        pion = Piece(7, 2, Data.RED)
        pion.make_king()
        self.board[7][2] = (pion)

        # pion2 = Piece(6, 7, Data.RED)
        # pion2.make_king()
        # self.board[6][7] = (pion2)