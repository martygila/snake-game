import pygame
import random
import sys

# Inizializzazione
pygame.init()

# Costanti
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20

WIDTH = GRID_WIDTH * CELL_SIZE
HEIGHT = GRID_HEIGHT * CELL_SIZE

FPS = 10

# Colori
BLACK = (30, 30, 30)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
RED = (220, 50, 50)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 36)


def random_food(snake):
    while True:
        food = (
            random.randint(0, GRID_WIDTH - 1),
            random.randint(0, GRID_HEIGHT - 1),
        )
        if food not in snake:
            return food


def draw_text(text, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


def reset_game():
    snake = [(10, 10)]
    direction = (1, 0)
    food = random_food(snake)
    score = 0
    return snake, direction, food, score


snake, direction, food, score = reset_game()

game_over = False

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

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

        head_x, head_y = snake[0]
        dx, dy = direction
        new_head = (head_x + dx, head_y + dy)

        # Collisione con il muro
        if (
            new_head[0] < 0
            or new_head[0] >= GRID_WIDTH
            or new_head[1] < 0
            or new_head[1] >= GRID_HEIGHT
        ):
            game_over = True

        # Collisione con se stesso
        elif new_head in snake:
            game_over = True

        else:
            snake.insert(0, new_head)

            if new_head == food:
                score += 1
                food = random_food(snake)
            else:
                snake.pop()

    # Disegno
    screen.fill(BLACK)

    # Cibo
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

    # Serpente
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
