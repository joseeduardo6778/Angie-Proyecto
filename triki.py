import pygame
import sys
import random

# Inicializar pygame
pygame.init()

# Dimensiones de la ventana
WIDTH, HEIGHT = 500, 650  
LINE_WIDTH = 10
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Nuevos colores que combinan
BG_COLOR = (247,244,227)
LINE_COLOR = (74,98,125)
CIRCLE_COLOR = (195,119,122)
CROSS_COLOR = (37,118,105)
TEXT_COLOR = (0,0,0)
BUTTON_COLOR = (93,133,172)
BUTTON_HOVER_COLOR = (93,133,172)
BUTTON_TEXT_COLOR = (255, 255, 255)
WINNER_TEXT_COLOR = (35,145,15)

# Configurar fuentes
font = pygame.font.SysFont("Arial", 30)
winner_font = pygame.font.SysFont("Arial", 40)

# Inicializar la pantalla con opción resizable
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Triki")

# Crear el tablero
board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Variables de juego
player = "X"
game_over = False
winner = None
game_mode = None  # Añadir una variable para el modo de juego

# Función para dibujar el menú
def draw_menu():
    screen.fill(BG_COLOR)
    title_font = pygame.font.SysFont("Arial", 40)
    menu_font = pygame.font.SysFont("Arial", 30)
    
    title_label = title_font.render("Menu Principal", True, TEXT_COLOR)
    screen.blit(title_label, (WIDTH // 2 - title_label.get_width() // 2, 50))

    human_vs_human_button = pygame.Rect(WIDTH // 2 - 119, 150, 250, 50)
    human_vs_ai_button = pygame.Rect(WIDTH // 2 - 119, 250, 250, 50)
    quit_button = pygame.Rect(WIDTH // 2 - 100, 450, 200, 50)

    pygame.draw.rect(screen, BUTTON_COLOR, human_vs_human_button)
    pygame.draw.rect(screen, BUTTON_COLOR, human_vs_ai_button)
    pygame.draw.rect(screen, BUTTON_COLOR, quit_button)

    human_vs_human_label = menu_font.render("Hombre vs Hombre", True, BUTTON_TEXT_COLOR)
    human_vs_ai_label = menu_font.render("Hombre vs Máquina", True, BUTTON_TEXT_COLOR)
    quit_label = menu_font.render("Salir", True, BUTTON_TEXT_COLOR)

    screen.blit(human_vs_human_label, (WIDTH // 2 - human_vs_human_label.get_width() // 2, 160))
    screen.blit(human_vs_ai_label, (WIDTH // 2 - human_vs_ai_label.get_width() // 2, 260))
    screen.blit(quit_label, (WIDTH // 2 - quit_label.get_width() // 2, 460))

    pygame.display.update()

    return human_vs_human_button, human_vs_ai_button, quit_button

# Dibujar el tablero de juego
def draw_board():
    screen.fill(BG_COLOR)
    
    for row in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), LINE_WIDTH)
    for col in range(1, BOARD_COLS):
        pygame.draw.line(screen, LINE_COLOR, (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, WIDTH), LINE_WIDTH)

    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == "O":
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == "X":
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)

# Verificar ganador
def check_winner():
    global winner
    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] is not None:
            winner = board[row][0]
            return True

    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            winner = board[0][col]
            return True

    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        winner = board[0][0]
        return True

    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        winner = board[0][2]
        return True

    return False

# Dibujar el texto del turno o del ganador
def draw_text():
    if game_over:
        text = f"Ganador: {winner}" if winner else "Empate"
        label = winner_font.render(text, True, WINNER_TEXT_COLOR)
    else:
        text = f"Turno de: {player}"
        label = font.render(text, True, TEXT_COLOR)
    
    screen.blit(label, (20, WIDTH + 20))

# Reiniciar el juego
def reset_game():
    global board, player, game_over, winner
    board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    player = "X"
    game_over = False
    winner = None

def draw_buttons(mouse_pos):
    button_width = 160
    button_height = 40
    button_spacing = 20  # Espacio entre botones

    total_button_width = button_width * 3 + button_spacing * 2
    start_x = (WIDTH - total_button_width) // 2

    reset_button = pygame.Rect(start_x, WIDTH + 60, button_width, button_height)
    menu_button = pygame.Rect(start_x + button_width + button_spacing, WIDTH + 60, button_width, button_height)
    quit_button = pygame.Rect(start_x + 2 * (button_width + button_spacing), WIDTH + 60, button_width, button_height)

    # Cambiar color cuando el mouse esté sobre el botón
    if reset_button.collidepoint(mouse_pos):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, reset_button)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, reset_button)

    if menu_button.collidepoint(mouse_pos):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, menu_button)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, menu_button)

    if quit_button.collidepoint(mouse_pos):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, quit_button)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, quit_button)

    # Renderizar texto de los botones
    reset_label = font.render("Reiniciar", True, BUTTON_TEXT_COLOR)
    menu_label = font.render("Volver Menú", True, BUTTON_TEXT_COLOR)
    quit_label = font.render("Salir", True, BUTTON_TEXT_COLOR)

    # Posicionar texto sobre cada botón
    screen.blit(reset_label, (reset_button.x + (button_width - reset_label.get_width()) // 2, reset_button.y + 5))
    screen.blit(menu_label, (menu_button.x + (button_width - menu_label.get_width()) // 2, menu_button.y + 5))
    screen.blit(quit_label, (quit_button.x + (button_width - quit_label.get_width()) // 2, quit_button.y + 5))

    return reset_button, menu_button, quit_button



# Manejar los clics del ratón
def handle_click(pos):
    global player, game_over

    if pos[1] < WIDTH and not game_over:
        col = pos[0] // SQUARE_SIZE
        row = pos[1] // SQUARE_SIZE

        if board[row][col] is None:
            board[row][col] = player
            if check_winner():
                game_over = True
            elif all(board[row][col] is not None for row in range(BOARD_ROWS) for col in range(BOARD_COLS)):
                game_over = True
            else:
                player = "O" if player == "X" else "X"

def main():
    global game_mode, WIDTH, HEIGHT

    in_menu = True
    while True:
        mouse_pos = pygame.mouse.get_pos()

        if in_menu:
            human_vs_human_button, human_vs_ai_button, quit_button = draw_menu()
        else:
            draw_board()
            draw_text()
            reset_button, menu_button, quit_button = draw_buttons(mouse_pos)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if in_menu:
                    if human_vs_human_button.collidepoint(event.pos):
                        in_menu = False
                        game_mode = "HUMAN_VS_HUMAN"
                    elif human_vs_ai_button.collidepoint(event.pos):
                        in_menu = False
                        game_mode = "HUMAN_VS_AI"
                    elif quit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                else:
                    if reset_button.collidepoint(event.pos):
                        reset_game()
                    elif menu_button.collidepoint(event.pos):
                        reset_game()
                        in_menu = True
                    elif quit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                    else:
                        handle_click(event.pos)


# Manejar los clics del ratón
def handle_click(pos):
    global player, game_over

    if pos[1] < WIDTH and not game_over:
        col = pos[0] // SQUARE_SIZE
        row = pos[1] // SQUARE_SIZE

        if board[row][col] is None:
            board[row][col] = player
            if check_winner():
                game_over = True
            elif all(board[row][col] is not None for row in range(BOARD_ROWS) for col in range(BOARD_COLS)):
                game_over = True
            else:
                player = "O" if player == "X" else "X"

                # Si el modo es "Hombre vs Máquina", la máquina hace su movimiento
                if game_mode == "HUMAN_VS_AI" and not game_over and player == "O":
                    ai_move()

# Función para el movimiento de la máquina
def ai_move():
    global player, game_over

    # Elegir un movimiento al azar de las posiciones disponibles
    available_moves = [(r, c) for r in range(BOARD_ROWS) for c in range(BOARD_COLS) if board[r][c] is None]
    if available_moves:
        row, col = random.choice(available_moves)
        board[row][col] = player

        if check_winner():
            game_over = True
        elif all(board[row][col] is not None for row in range(BOARD_ROWS) for col in range(BOARD_COLS)):
            game_over = True
        else:
            player = "X"  # Cambiar de turno al jugador


if __name__ == "__main__":
    main()
