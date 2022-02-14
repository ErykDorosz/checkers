import pygame
import sys



#######################   Adres IP należy zmienić w linii 88    ###############################


import socket
import pickle
from _thread import *

from Board import Board
from Data import Data
from Game import Game

    ####################
    # Zmienne globalne #
    ####################

is_client_connected = False
client = None
addr = None
run = False
x, y = Data.WIDTH // 4 - 50, Data.HEIGHT // 4
FPS = 60

WIN = pygame.display.set_mode((Data.WIDTH, Data.HEIGHT))
pygame.display.set_caption('Server')
pygame.display.flip()

    #########################################################
    # Metoda zwracająca współrzędne pola klikniętego myszką #
    #########################################################

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // Data.SQUARE_SIZE
    col = x // Data.SQUARE_SIZE
    return row, col

    ########################################
    # Wątek odbierający planszę od klienta #
    ########################################

def data_thread(client, game):
    global run
    while True:
        try:
            data = client.recv(4000)
            if data:
                received_board = pickle.loads(data)
                game.board.change_to_board(received_board)
                game.change_turn()
                pygame.display.update()
        except Exception as e:
            run = False

    ##########################################
    # Wątek oczekujący na dołączenie klienta #
    ##########################################

def listen_thread(server):
    global is_client_connected, client, addr
    client, addr = server.accept()
    is_client_connected = True

        ########
    ##### MAIN #####
        ########

def main():
    global is_client_connected
    global run
    pygame.init()

    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    game.display_text('OCZEKIWANIE NA PRZECIWNIKA', x, y)
    row, col = -1, -1

    ###########################################
    # Uruchomienie połączenia poprzez gniazdo #
    ###########################################

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind( ('25.68.65.107', 3999) )
    server.listen()
    start_new_thread(listen_thread, (server,))

    ##########################
    # Oczekiwanie na klienta #
    ##########################

    while not is_client_connected:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('Quitting!')
                pygame.quit()
                sys.exit()

    start_new_thread(data_thread, (client, game))

    send_board = []
    send = True

    ####################
    # Petla glowna gry #
    ####################

    while run:
        clock.tick(FPS)

        ########################################
        # Obsługa po wygranej jednego z graczy #
        ########################################

        if game.winner() is not None:
            if game.winner() == Data.WHITE:
                send_board = Board.change_to_send_board(game.board)
                data = pickle.dumps(send_board)
                client.send(data)

            send = False
            WIN.fill(Data.BLACK)
            game.display_text("Wygrały:  ", x, y - 50)
            font = pygame.font.Font('freesansbold.ttf', 32)
            if game.winner() == Data.WHITE:
                WIN.blit(font.render("BIAŁE", True, Data.WHITE), (x + 200, y - 50))
            else:
                WIN.blit(font.render("CZERWONE", True, Data.RED), (x + 200, y - 50))

            game.display_text("R - restart", x + 130, y + 50)
            pygame.display.update()
            r = True

            ######################
            # Propozycja rewanzu #
            ######################

            while r:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            game.reset()
                            send_board = Board.change_to_send_board(game.board)
                            data = pickle.dumps(send_board)
                            client.send(data)
                            r = False

        #####################################
        # Obsługa podczas ruchu przeciwnika #
        #####################################

        if game.turn == Data.RED:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            if send:
                data = pickle.dumps(send_board)
                client.send(data)
                send = False

        #####################################
        # Obsługa podczas wykonywania ruchu #
        #####################################

        if game.turn == Data.WHITE:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    row, col = get_row_col_from_mouse(pos)
                    game.select(row, col)

            send_board = Board.change_to_send_board(game.board)
            game.update(row, col)
            send = True

    #######################################################################################
    # Informacja o utraceniu połączenia z klientem wraz z możliwością zamknięcia programu #
    #######################################################################################

    WIN.fill(Data.BLACK)
    game.display_text("UTRACONO POŁĄCZENIE!", x, y)
    game.display_text("Q - wyjście", x + 130, y + 50)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    return


main()
