import sys
from snake_constants import *
from snake_functions import *

# Initialize all import pygame modules
pygame.init()

# Game window creation
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

# Timer
clock = pygame.time.Clock()

# Font for text
font = pygame.font.SysFont(None, 36)

# Function to draw white text
def draw_text(text: str, color: tuple[int, int, int], x: int, y: int) -> None:
    """
    Input:
        text: string representing the text to display
        color: tuple representing the color of the text (R, G, B)
        x: x-coordinate of the text position
        y: y-coordinate of the text position
    Output:
        None
    """
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~ 6 ~ 7 ~ 8 ~ 9 ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~
# ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~ 6 ~GAME START ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~
# ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~ 6 ~ 7 ~ 8 ~ 9 ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~

# Initialization of snake first position, first direction, food position and score = 0
snake, direction, food, score = reset_game()

game_over = False

while True:
    # ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~ 6 ~ 7 ~
    # ~ 1 ~EVENT MANAGER CYCLE~ 7 ~
    # ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~ 6 ~ 7 ~
    for event in pygame.event.get():
        # Generated event from closing X button
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Generated event from any keyboard key
        if event.type == pygame.KEYDOWN:
            
            if game_over:
                if event.key == pygame.K_r:
                    snake, direction, food, score = reset_game()
                    game_over = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            else:
                if event.key == pygame.K_UP and direction != (0, 1):
                    direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)

    if not game_over:

        head_x, head_y = snake[0]                   # Head position given by snake list
        dx, dy = direction                          # Direction vector given by direction tuple
        new_head = (head_x + dx, head_y + dy)       # New head position

        # Check wall collision
        if (
            new_head[0] < 0
            or new_head[0] >= GRID_WIDTH
            or new_head[1] < 0
            or new_head[1] >= GRID_HEIGHT
        ):
            game_over = True
        # Check self collision
        elif new_head in snake:
            game_over = True
        # Otherwise update the snake position
        else:
            # Insert a tile in snake in first position using the new_head coordinates
            snake.insert(0, new_head)
            # If the new head is in the same position of food, add score and put another food
            if new_head == food:
                score += 1
                food = random_food(snake)
            # Otherwise it removes the tail (last element), previously added
            else:
                snake.pop()

    # Background design
    #screen.fill(BLACK)
    chess_background(screen, ORANGE)

    # Food design
    pygame.draw.rect(
        screen,
        RED,
        (
            food[0] * CELL_SIZE,
            food[1] * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE,
        ),
    )

    # Snake design
    for i, segment in enumerate(snake):
        color = GREEN if i == 0 else DARK_GREEN
        pygame.draw.rect(
            screen,
            color,
            (
                segment[0] * CELL_SIZE,
                segment[1] * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE,
            ),
        )

    draw_text(f"Punteggio: {score}", WHITE, 10, 10)

    if game_over:
        draw_text("GAME OVER", RED, WIDTH // 2 - 90, HEIGHT // 2 - 40)
        draw_text("R = Ricomincia", WHITE, WIDTH // 2 - 100, HEIGHT // 2 + 10)
        draw_text("ESC = Esci", WHITE, WIDTH // 2 - 80, HEIGHT // 2 + 50)

    pygame.display.flip()
    clock.tick(FPS)
