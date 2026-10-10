import random, pygame, sys
from collections.abc import Callable
from snake_constants import *

# ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~ 6 ~ 7 ~ 8 ~ 9 ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~
# ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~ 6 ~ GAME LOGIC~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~
# ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~ 6 ~ 7 ~ 8 ~ 9 ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~

# Function to generate a random position to food
def random_food(snake: tuple) -> tuple[int, int]:
    """
    Generate a new food position until the new position is not above the snake position
    Input:
        snake: tuple list that gives the snake position.
    Output:
        food: tuple representing the food position
    """
    while True:
        food = (
            random.randint(0, GRID_WIDTH - 1),
            random.randint(0, GRID_HEIGHT - 1),
        )
        if food not in snake:
            return food

# Function to set/reset game
def reset_game() -> tuple[list[tuple[int, int]], tuple[int, int], tuple[int, int], int]:
    """
    Input:
        None
    Output:
        snake: list of tuples representing the snake positions starting from a single segment at the center of the grid (10,10)
        direction: tuple representing the initial direction of the snake (1, 0) (right)
        food: tuple representing the food position
        score: int representing the current score
    """
    snake = [(10, 10)]
    direction = (1, 0)
    food = random_food(snake)
    score = 0
    return snake, direction, food, score

# Function to draw white text
def draw_text(font: pygame.font.SysFont,
              screen: pygame.Surface,
              text: str,
              color: tuple[int, int, int],
              x: int, y: int) -> None:
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

def quit_game(screen: pygame.Surface,
              font: pygame.font.SysFont,
              clock: pygame.time.Clock) -> None:
    pygame.quit()
    sys.exit()

def void(screen: pygame.Surface,
        font: pygame.font.SysFont,
        clock: pygame.time.Clock) -> None:
    pass

# ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~ 6 ~ 7 ~ 8 ~ 9 ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~
# ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~ DESIGN FUNCTIONS  ~ 2 ~ 3 ~ 4 ~ 5 ~
# ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~ 6 ~ 7 ~ 8 ~ 9 ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~

def unified_background(screen: pygame.Surface, colors: list[tuple[tuple[int,int,int], ...]]) -> None:
    pass


def chess_background(screen: pygame.Surface, colors: list[tuple[tuple[int,int,int], ...]]):
    for i in range(0, WIDTH, CELL_SIZE):
        for j in range(0, HEIGHT, CELL_SIZE):
            if (i // CELL_SIZE + j // CELL_SIZE) % 2 == 0:
                pygame.draw.rect(screen, colors[0], (i, j, CELL_SIZE, CELL_SIZE))
            else:
                if not (len(colors) == 1 or colors[1] is None):
                    pygame.draw.rect(screen, colors[1], (i, j, CELL_SIZE, CELL_SIZE))
                else:
                    pygame.draw.rect(screen, (colors[0][1] // 2, colors[0][1] // 2, colors[0][2] // 2), (i, j, CELL_SIZE, CELL_SIZE))

background_functions = {'chess': chess_background}