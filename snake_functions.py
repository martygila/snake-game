import random, pygame, sys, math
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
    # Use SDL2's alpha blitter to preserve the text's transparent background.
    screen.blit(img, (x, y), special_flags=pygame.BLEND_ALPHA_SDL2)

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
                    pygame.draw.rect(screen, tuple(channel // 2 for channel in colors[0]), (i, j, CELL_SIZE, CELL_SIZE))

background_functions = {'chess': chess_background}

# ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~ 6 ~ 7 ~ 8 ~ 9 ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~
# ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~ HIGH SCORES FUNCTIONS ~ 3 ~ 4 ~ 5 ~
# ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~ 6 ~ 7 ~ 8 ~ 9 ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~

# Fuction that asks for player name

def insert_player_name(screen: pygame.Surface, font: pygame.font.SysFont, clock: pygame.time.Clock) -> str | None:
    name = ""
    max_length = 6

    pygame.key.start_text_input()
    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.TEXTINPUT:
                    for c in event.text:
                        if c.isalnum():
                            name = name + c
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif event.key == pygame.K_RETURN and name:
                        return name[:max_length]
                    elif event.key == pygame.K_ESCAPE:
                        return None
            
            screen.fill(ORANGE)
            draw_text(font, screen, "Inserisci il nome del giocatore (max 6 caratteri)", BLACK, 40, 100)
            draw_text(font, screen, name + "_", DARK_GREEN, 40, 160)

            pygame.display.update()
            clock.tick(30)
    finally:
        pygame.key.stop_text_input()


# Function to insert a new high score
def save_high_score(name: str, score: int, high_scores: list[list[str],list[int]]):
    if score > high_scores[1][-1]:
        for i in range(N_SCORES):
            if score > high_scores[1][i]:
                high_scores[0].insert(i, name)
                high_scores[1].insert(i, score)
                high_scores[:] = high_scores[:][:N_SCORES]
                break
        with open('high_scores.txt', 'w') as f:
            for i in range(N_SCORES):
                f.write(f"{high_scores[0][i]}   {high_scores[1][i]}\n")

    return None

# Function to read the high scores
def read_high_scores():
    high_scores = [[], []]
    with open('high_scores.txt', 'r') as f:
        for line in f:
            line = line.strip().split()
            high_scores[0].append(line[0])
            high_scores[1].append(int(line[1]))

    return high_scores
