from snake_constants import *
from snake_functions import *

button_width = CELL_SIZE * 9
button_height = CELL_SIZE * 3

# ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~ 6 ~ 7 ~ 8 ~ 9 ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~
# ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~ 6 ~ GAME LOOP ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~
# ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~ 6 ~ 7 ~ 8 ~ 9 ~ 1 ~ 2 ~ 3 ~ 4 ~ 5 ~


"""
The ButtonPanel is a class used to create menu with buttons.
It is declared by giving the buttons variable: a dictionary that stores the button name
(same of the string to print above the button) as key and the function that must perform as value.
The other variables to give as input are the screen, the font and the clock.
The variable draw_buttons or d_b is a dictionary containing the button name as key and a set 
with the function that perform and the pygame.Rect (in this order) as values.
"""
class ButtonPanel:
    def __init__(self, buttons: dict[str,function],
                 screen: pygame.Surface,
                 font: pygame.font.SysFont,
                 clock: pygame.time.Clock,
                 mouse: tuple[int, int]):
        self.buttons = buttons
        self.screen = screen
        self.font = font
        self.clock = clock
        self.mouse = mouse

        d_b = self.define_buttons(self)
        self.draw_buttons(self,d_b)

    def define_buttons(self) -> dict[str,set[function,pygame.Rect]]:
        N_buttons = len(self.buttons)
        draw_buttons = dict.fromkeys(self.buttons.keys())
        for index,button in enumerate(self.buttons.keys()):
            rectangle = pygame.Rect(WIDTH // 2 - button_width // 2,
                                               HEIGHT // 2 - button_width // 2 - (index - N_buttons // 2) * (N_buttons // 2) * button_width,
                                               button_width,
                                               button_height)
            draw_buttons[button] = {self.buttons[button], rectangle}
        return draw_buttons
    
    def draw_buttons(self, buttons: dict[str,set[function,pygame.Rect]]) -> None:
        for index, button in enumerate(buttons.keys()):
            if index == 0:
                c1, c2 = (RED_LIGHT, RED)
            elif index == 1:
                c1, c2 = (GREEN, DARK_GREEN)
            else:
                c1, c2 = (GREEN_LIGHT, GREEN)
            pygame.draw.rect(self.screen,
                             c1 if buttons[button].collide(self.mouse) else c2,
                             buttons[button])
            draw_text(self.font,
                      self.screen,
                      button,
                      WHITE,
                      buttons[button].x+20,
                      buttons[button].y+10)

"""
ButtonEventHandler class
"""
class ButtonEventHandler:
    def __init__(self, buttons: dict[str,set[function,pygame.Rect]],
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
        for _, values in self.buttons.values():
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if values[1].collidepoint(self.mouse):
                        values[0](self.screen, self.font, self.clock)



def menu_start(screen: pygame.Surface, font: pygame.font.SysFont, clock: pygame.time.Clock) -> None:
    while True:
        screen.fill(BG)
        mouse = pygame.mouse.get_pos()

        play_button = pygame.Rect(WIDTH // 2 - button_width // 2,
                                 (HEIGHT // 2 - button_height * 3 // 2) - button_height // 2,
                                 button_width,
                                 button_height)
        settings_button = pygame.Rect(WIDTH // 2 - button_width // 2,
                                      HEIGHT // 2 - button_height // 2,
                                      button_width,
                                      button_height)
        quit_button = pygame.Rect(WIDTH // 2 - button_width // 2, 
                                  (HEIGHT // 2 + button_height * 3 // 2) - button_height // 2,
                                  button_width,
                                  button_height)

        pygame.draw.rect(screen, RED_LIGHT if play_button.collidepoint(mouse) else RED, play_button)
        pygame.draw.rect(screen, GREEN if settings_button.collidepoint(mouse) else DARK_GREEN, settings_button)
        pygame.draw.rect(screen, GREEN_LIGHT if quit_button.collidepoint(mouse) else GREEN, quit_button)

        draw_text(font, screen, "Play", WHITE, play_button.x + 20, play_button.y + 10)
        draw_text(font, screen, "Settings", WHITE, settings_button.x + 20, settings_button.y + 10)
        draw_text(font, screen, "Quit", WHITE, quit_button.x + 20, quit_button.y + 10)


        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(mouse):
                    main_game_loop(screen, font, clock)
                elif settings_button.collidepoint(mouse):
                    menu_setting(screen, font, clock)
                elif quit_button.collidepoint(mouse):
                    pygame.quit()
                    sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    main_game_loop(screen, font, clock)

                if event.key == pygame.K_s:
                    menu_setting(screen, font, clock)

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

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

        background_button = pygame.Rect(WIDTH // 2 - button_width // 2,
                                        HEIGHT // 2 - button_height // 2,
                                        button_width,
                                        button_height)
        return_button = pygame.Rect(WIDTH // 2 - button_width // 2,
                                                HEIGHT - button_height * 3 // 2,
                                                button_width,
                                                button_height)

        pygame.draw.rect(screen, GREEN if background_button.collidepoint(mouse) else DARK_GREEN, background_button)
        pygame.draw.rect(screen, RED_LIGHT if return_button.collidepoint(mouse) else RED, return_button)

        draw_text(font, screen, "Background", WHITE, background_button.x + 20, background_button.y + 10)
        draw_text(font, screen, "Return", WHITE, return_button.x + 20, return_button.y + 10)

        for event in pygame.event.get():
        
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if background_button.collidepoint(mouse):
                    pass
                elif return_button.collidepoint(mouse):
                    menu_start(screen, font, clock)
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    pass
                if event.type == pygame.K_r:
                    menu_start(screen, font, clock)
        

        pygame.display.update()

