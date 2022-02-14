class Data:
    WIDTH, HEIGHT = 800, 900        # Wymiary okna gry
    ROWS, COLS = 8, 8               # Ilość wierszy i kolumn planszy
    SQUARE_SIZE = WIDTH // COLS     # Długość boku pojedynczego pola

    ##########
    # Kolory #
    ##########

    RED = (255, 0, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    GREY = (128, 128, 128)
    GOLD = (244, 196, 48)
    GREEN = (0, 255, 0)
    SKYBLUE = (0, 191, 255)

    ##########################
    # Parametry wyświetlania #
    ##########################

    PADDING = 20
    OUTLINE = 2

    ############
    # Kierunki #
    ############

    TOPLEFT = 1
    TOPRIGHT = 2
    BOTLEFT = 3
    BOTRIGHT = 4
