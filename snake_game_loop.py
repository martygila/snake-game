from snake_constants import *
from snake_functions import *

button_width = CELL_SIZE * 9
button_height = CELL_SIZE * 3

type ButtonAction = Callable[[pygame.Surface, pygame.font.Font, pygame.time.Clock], None]
type ButtonData = tuple[ButtonAction, pygame.Rect]


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
    def __init__(self,
                 screen: pygame.Surface,
                 font: pygame.font.SysFont,
                 clock: pygame.time.Clock,
                 mouse: tuple[int, int]):
        self.screen = screen
        self.font = font
        self.clock = clock
        self.mouse = mouse

    def define_buttons(self,  buttons: dict[str,ButtonAction]) -> dict[str,ButtonData]:
        N_buttons = len(buttons)
        draw_buttons = {}
        for index,button in enumerate(buttons.keys()):
            rect = pygame.Rect(WIDTH // 2 - button_width // 2,
                                    HEIGHT // 2 - button_width // 2 + ((index+1) - N_buttons // 2) * ( 1 + button_width // 2),
                                    button_width,
                                    button_height)
            draw_buttons[button] = (buttons[button], rect)
        return draw_buttons
    
    def draw_buttons(self, buttons: dict[str,ButtonData], selected_index: int) -> None:
        for index, button in enumerate(buttons.keys()):
            if index == 0:
                hover_color, normal_color = (RED_LIGHT, RED)
            elif index == 1:
                hover_color, normal_color = (GREEN, DARK_GREEN)
            else:
                hover_color, normal_color = (GREEN_LIGHT, GREEN)
            _, rect = buttons[button]
            hovered = rect.collidepoint(self.mouse)
            selected = index == selected_index
            pygame.draw.rect(self.screen,
                             hover_color if hovered or selected else normal_color,
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
    def __init__(self,
                 screen: pygame.Surface,
                 font: pygame.font.SysFont,
                 clock: pygame.time.Clock):
        self.screen = screen
        self.font = font
        self.clock = clock
        self.selected_index = 0
    def assing_event(self, buttons: dict[str,ButtonData]):
        button_names = list(buttons.keys())
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and len(button_names) != 0:
                if event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(button_names)
                elif event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(button_names)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    action, _ = buttons[button_names[self.selected_index]]
                    action(self.screen, self.font, self.clock)
            if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for action, rect in buttons.values():
                    if rect.collidepoint(event.pos):
                        action(self.screen, self.font, self.clock)
                        break

# ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~ 6 ~ 7 ~ 8 ~ 9 ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~
# ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~ 6 ~ GAME LOOP ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~
# ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~ 6 ~ 7 ~ 8 ~ 9 ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~

def menu_start(screen: pygame.Surface, font: pygame.font.SysFont, clock: pygame.time.Clock) -> None:
    buttonhandler = ButtonEventHandler(screen, font, clock)
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
        buttonpanel = ButtonPanel(screen, font, clock, mouse)
        # Define all the given buttons
        definedbutton = buttonpanel.define_buttons(buttons)
        # Draw the defined buttons
        buttonpanel.draw_buttons(definedbutton, buttonhandler.selected_index)
        # Manage the button events
        buttonhandler.assing_event(definedbutton)

        pygame.display.update()

def menu_setting(screen: pygame.Surface, font: pygame.font.SysFont, clock: pygame.time.Clock):
    buttonhandler = ButtonEventHandler(screen, font, clock)
    while True:
        screen.fill(BG)
        mouse = pygame.mouse.get_pos()

        buttons = {
            'Background': void,
            'Return': menu_start,
        }

        buttonpanel = ButtonPanel(screen, font, clock, mouse)
        definedbutton = buttonpanel.define_buttons(buttons)
        buttonpanel.draw_buttons(definedbutton, buttonhandler.selected_index)
        buttonhandler.assing_event(definedbutton)
        

        pygame.display.update()



# ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~ 6 ~ 7 ~ 8 ~ 9 ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~
# ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~ GAME MECHANIC ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~
# ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~ 6 ~ 7 ~ 8 ~ 9 ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~



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
                    elif event.key == pygame.K_m:
                        menu_start(screen, font, clock)
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
        chess_background(screen, BLACK, )

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
            draw_text(font, screen, "GAME OVER", RED, WIDTH // 2 - 90, HEIGHT // 2 - 80)
            draw_text(font, screen, "R = Ricomincia", WHITE, WIDTH // 2 - 100, HEIGHT // 2 -30)
            draw_text(font, screen, "M = Menù", WHITE, WIDTH // 2 - 70, HEIGHT // 2 + 10)
            draw_text(font, screen, "ESC = Esci", WHITE, WIDTH // 2 - 80, HEIGHT // 2 + 50)

        pygame.display.flip()
        clock.tick(5+10*math.log(score+1,20))  # Adjust the speed of the game based on the cell size