from snake_constants import *
from snake_functions import *

button_width = CELL_SIZE * 9
button_height = CELL_SIZE * 3

type ButtonAction = Callable[[pygame.Surface, pygame.font.Font, pygame.time.Clock], None]
type ButtonData = tuple[ButtonAction, pygame.Rect]

# ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~ 6 ~ 7 ~ 8 ~ 9 ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~
# ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~ 6 ~ GAME LOOP ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~
# ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~ 6 ~ 7 ~ 8 ~ 9 ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~


"""
The ButtonPanel is a class used to create menu with buttons.
It is declared by giving the buttons variable: a dictionary that stores the button name
(same of the string to print above the button) as key and a new variable called ButtonAction
which store the function that the button must perform.
The other variables to give as input are the screen, the font and the clock.
Another variable is used, referred as draw_button. It is used to store the information about
the button name and another variable called ButtonData. The latter is a tuple containing the button
action and the drawed rectangle.
"""
class ButtonPanel:
    def __init__(self, buttons: dict[str,ButtonAction],
                 screen: pygame.Surface,
                 font: pygame.font.SysFont,
                 clock: pygame.time.Clock,
                 mouse: tuple[int, int]):
        self.buttons = buttons
        self.screen = screen
        self.font = font
        self.clock = clock
        self.mouse = mouse

    def define_buttons(self) -> dict[str,ButtonData]:
        N_buttons = len(self.buttons)
        draw_buttons = {}
        for index,button in enumerate(self.buttons.keys()):
            rectangle = pygame.Rect(WIDTH // 2 - button_width // 2,
                                    HEIGHT // 2 - button_width // 2 + ((index+1) - N_buttons // 2) * ( 1 + button_width // 2),
                                    button_width,
                                    button_height)
            draw_buttons[button] = (self.buttons[button], rectangle)
        return draw_buttons
    
    def draw_buttons(self, buttons: dict[str,ButtonData]) -> None:
        for index, button in enumerate(buttons.keys()):
            if index == 0:
                hover_color, normal_color = (RED_LIGHT, RED)
            elif index == 1:
                hover_color, normal_color = (GREEN, DARK_GREEN)
            else:
                hover_color, normal_color = (GREEN_LIGHT, GREEN)
            _, rect = buttons[button]
            hovered = rect.collidepoint(self.mouse)
            pygame.draw.rect(self.screen,
                             hover_color if hovered else normal_color,
                             rect)
            draw_text(self.font,
                      self.screen,
                      button,
                      WHITE,
                      rect.x+20,
                      rect.y+10)

"""
ButtonEventHandler class
This class utilizes the new variable ButtonData.
It is used to manage all the event to perform inside buttons.
"""
class ButtonEventHandler:
    def __init__(self, buttons: dict[str,ButtonData],
                 screen: pygame.Surface,
                 font: pygame.font.SysFont,
                 clock: pygame.time.Clock,
                 mouse: tuple[int, int]):
        self.buttons = buttons
        self.screen = screen
        self.font = font
        self.clock = clock
        self.mouse = mouse
    def assing_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for action, rect in self.buttons.values():
                    if rect.collidepoint(self.mouse):
                        action(self.screen, self.font, self.clock)
                        break



def menu_start(screen: pygame.Surface, font: pygame.font.SysFont, clock: pygame.time.Clock) -> None:
    while True:
        screen.fill(BG)
        mouse = pygame.mouse.get_pos()

        # Buttons inside the menu_start and their actions
        buttons = {
            'Play': main_game_loop,
            'Settings': menu_setting,
            'Quit': quit_game
        }
        # Initilize the buttonpanel
        buttonpanel = ButtonPanel(buttons, screen, font, clock, mouse)
        # Define all the given buttons
        definedbutton = buttonpanel.define_buttons()
        # Draw the defined buttons
        buttonpanel.draw_buttons(definedbutton)
        # Manage the button events
        buttonhandler = ButtonEventHandler(definedbutton, screen, font, clock, mouse)
        buttonhandler.assing_event()

        pygame.display.update()

def main_game_loop(screen: pygame.Surface, font: pygame.font.SysFont, clock: pygame.time.Clock) -> None:
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
        screen.fill(BLACK)
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

        draw_text(font, screen, f"Punteggio: {score}", WHITE, 10, 10)

        if game_over:
            draw_text(font, screen, "GAME OVER", RED, WIDTH // 2 - 90, HEIGHT // 2 - 40)
            draw_text(font, screen, "R = Ricomincia", WHITE, WIDTH // 2 - 100, HEIGHT // 2 + 10)
            draw_text(font, screen, "ESC = Esci", WHITE, WIDTH // 2 - 80, HEIGHT // 2 + 50)

        pygame.display.flip()
        clock.tick(FPS)

def menu_setting(screen: pygame.Surface, font: pygame.font.SysFont, clock: pygame.time.Clock):
    while True:
        screen.fill(BG)
        mouse = pygame.mouse.get_pos()

        buttons = {
            'Background': void,
            'Return': menu_start,
        }

        buttonpanel = ButtonPanel(buttons, screen, font, clock, mouse)
        definedbutton = buttonpanel.define_buttons()
        buttonpanel.draw_buttons(definedbutton)
        buttonhandler = ButtonEventHandler(definedbutton, screen, font, clock, mouse)
        buttonhandler.assing_event()
        

        pygame.display.update()

