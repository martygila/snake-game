import random, pygame

from snake_constants import *

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

def chess_background(screen: pygame.Surface, color: tuple[int, int, int], color2: tuple[int, int, int] = None):
    for i in range(0, WIDTH, CELL_SIZE):
        for j in range(0, HEIGHT, CELL_SIZE):
            if (i // CELL_SIZE + j // CELL_SIZE) % 2 == 0:
                pygame.draw.rect(screen, color, (i, j, CELL_SIZE, CELL_SIZE))
            else:
                if color2 is not None:
                    pygame.draw.rect(screen, color2, (i, j, CELL_SIZE, CELL_SIZE))
                else:
                    pygame.draw.rect(screen, (color[0] // 2, color[1] // 2, color[2] // 2), (i, j, CELL_SIZE, CELL_SIZE))