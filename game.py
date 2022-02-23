import random
import sys
from os import path

import pygame

from constants import *


class Game:
    
    def __init__(self) -> None:
        '''
        Game initialization
        '''
        pygame.mixer.pre_init()
        pygame.mixer.init()
        pygame.init()
        self.__canvas = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('The Snake')
        pygame.mouse.set_visible(False)
        self.__clock = pygame.time.Clock()

        # Preload fonts that we are going to use
        self.__font_sm = pygame.font.SysFont('Comic Sans MS', 16)
        self.__font_md = pygame.font.SysFont('Comic Sans MS', 20, True)
        self.__font_lg = pygame.font.SysFont('Comic Sans MS', 40, True, True)

        # Preload cursor texture
        self.__cursor = pygame.image.load(path.join(PATH, 'res', 'images', 'mouse_icon.png'))
        self.__cursor_rect = self.__cursor.get_rect()

        # Preload Main menu background texture
        self.__bg_texture = pygame.image.load(path.join(PATH, "res", 'images', "bg.png"))
        self.__bg_texture = pygame.transform.scale(self.__bg_texture, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.__bg_rect = self.__bg_texture.get_rect()

        # Preload game interface textures.
        self.__qc_menu_if_texture  = pygame.image.load(path.join(PATH, 'res', 'images', 'quit_menu_interface.png'))
        self.__mm_title_bg_texture = pygame.image.load(path.join(PATH, 'res', 'images', 'main_menu_title_bg.png'))
        self.__info_bg_texture  = pygame.image.load(path.join(PATH, 'res', 'images', 'info_interface.png'))
        self.__pause_interface_texture  = pygame.image.load(path.join(PATH, 'res', 'images', 'pause_interface.png'))
        self.__go_interface_texture  = pygame.image.load(path.join(PATH, 'res', 'images', 'game_over_interface.png'))
        self.__game_interface_texture  = pygame.image.load(path.join(PATH, 'res', 'images', 'game_interface.png'))

        self.__level_bar_start_texture = pygame.image.load(path.join(PATH, 'res', 'images', 'level_bar_start.png'))
        self.__level_bar_texture = pygame.image.load(path.join(PATH, 'res', 'images', 'level_bar.png'))
        self.__level_bar_end_texture = pygame.image.load(path.join(PATH, 'res', 'images', 'level_bar_end.png'))
        self.__health_bar_start = pygame.image.load(path.join(PATH, 'res', 'images', 'health_bar_start.png'))
        self.__health_bar = pygame.image.load(path.join(PATH, 'res', 'images', 'health_bar.png'))
        self.__health_bar_end = pygame.image.load(path.join(PATH, 'res', 'images', 'health_bar_end.png'))

        # Preload buttons textures
        self.__button_play_texture = pygame.image.load(path.join(PATH, 'res', 'images', 'buttons', 'button_play.png'))
        self.__button_info_texture  = pygame.image.load(path.join(PATH, 'res', 'images', 'buttons', 'button_info.png'))
        self.__button_quit_texture = pygame.image.load(path.join(PATH, 'res', 'images', 'buttons', 'button_quit.png'))
        self.__button_back_texture = pygame.image.load(path.join(PATH, 'res', 'images', 'buttons', 'button_back.png'))

        # Preload snake sprites. They should load at the beginning of the game
        self.__snake_head_sprite = pygame.image.load(path.join(PATH, 'res', 'images', 'snake_head.png'))
        self.__snake_head_sprite = pygame.transform.scale(self.__snake_head_sprite, (CELL_SIZE, CELL_SIZE))
        self.__snake_body_sprite = pygame.image.load(path.join(PATH, 'res', 'images', 'snake_body.png'))
        self.__snake_body_sprite = pygame.transform.scale(self.__snake_body_sprite, (CELL_SIZE, CELL_SIZE))
        self.__snake_curved_body_sprite = pygame.image.load(path.join(PATH, 'res', 'images', 'snake_curved_body.png'))
        self.__snake_curved_body_sprite = pygame.transform.scale(self.__snake_curved_body_sprite, (CELL_SIZE, CELL_SIZE))
        self.__snake_tail_sprite = pygame.image.load(path.join(PATH, 'res', 'images', 'snake_tile.png'))
        self.__snake_tail_sprite = pygame.transform.scale(self.__snake_tail_sprite, (CELL_SIZE, CELL_SIZE))

        # Preload apple sprite
        self.__red_apple_texture = pygame.image.load(path.join(PATH, 'res', 'images', 'red_apple.png'))
        self.__red_apple_texture = pygame.transform.scale(self.__red_apple_texture, (CELL_SIZE, CELL_SIZE))
        self.__red_apple_rect = self.__red_apple_texture.get_rect()

        # Preload sounds
        self.__mouse_click_sound = pygame.mixer.Sound(path.join(PATH, 'res', 'sounds', 'click.wav'))
        self.__snake_eat_sound = pygame.mixer.Sound(path.join(PATH, 'res', 'sounds', 'snake_eat.mp3'))
        self.__level_up_sound = pygame.mixer.Sound(path.join(PATH, 'res', 'sounds', 'oh_yeah.wav'))

        # Flag to control that the game is running
        self.__running = True
        # Game state
        self.__state = MENU

    def __play_click_sound(self):
        """ Plays mouse click sound """
        pygame.mixer.Channel(0).play(self.__mouse_click_sound)
        return

    def __update_cursor(self):
        """ Updates mouse cursor position """
        pos_raton = pygame.mouse.get_pos()
        self.__cursor_rect.topleft = pos_raton
        self.__canvas.blit(self.__cursor, self.__cursor_rect)
        return
        
    def __render_quit_menu_confirmation_screen(self):
        """ Renders the confirmation menu to quit the game """
        interface_rect = self.__qc_menu_if_texture.get_rect()
        interface_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        confirm_text = self.__font_md.render("Are you sure?", True, WHITE)
        
        # We get buttons rectangles
        cancel_button_rect  = pygame.Rect(SCREEN_WIDTH / 2 + 148, SCREEN_HEIGHT / 2 - 32, 32, 32)
        confirm_button_rect = pygame.Rect(SCREEN_WIDTH / 2 + 148, SCREEN_HEIGHT / 2, 32, 32)

        while True:
            for event in pygame.event.get():
                # No need to ask again, right?
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.__play_click_sound()
                    # We quit
                    if confirm_button_rect.collidepoint(event.pos):                    
                        pygame.quit()
                        sys.exit()
                    # We simply exit the loop to finish and return to the previous screen
                    elif cancel_button_rect.collidepoint(event.pos):
                        return
            
            self.__canvas.fill(BLACK)
            
            self.__canvas.blit(self.__qc_menu_if_texture, interface_rect)
            self.__canvas.blit(confirm_text, (SCREEN_WIDTH / 2 - 90, SCREEN_HEIGHT / 2 - 15))

            self.__update_cursor()
            pygame.display.flip()

    def __render_main_menu_screen(self):
        """ Renders the game main menu """

        # Gets button rectangles
        mm_title_bg_rect = self.__mm_title_bg_texture.get_rect()
        play_button_rect = self.__button_play_texture.get_rect()
        info_button_rect = self.__button_info_texture.get_rect()
        quit_button_rect = self.__button_quit_texture.get_rect()

        # We define the positions of each component of the screen
        self.__bg_rect.center   = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        mm_title_bg_rect.center = (SCREEN_WIDTH / 2, 50)
        play_button_rect.center = (SCREEN_WIDTH / 2 - 20, SCREEN_HEIGHT / 2 - 98)
        info_button_rect.center = (SCREEN_WIDTH / 2 - 22, SCREEN_HEIGHT / 2 - 18)
        quit_button_rect.center = (SCREEN_WIDTH / 2 - 20, SCREEN_HEIGHT / 2 + 67)
        
        title_text       = self.__font_lg.render("THE SNAKE", True, WHITE)
        play_button_text = self.__font_md.render("PLAY", True, WHITE)
        info_button_text = self.__font_md.render("INSTRUCTIONS", True, WHITE)
        quit_button_text = self.__font_md.render("QUIT", True, WHITE)

        # We execute this screen while 'state' is = MENU
        while self.__state == MENU:        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__render_quit_menu_confirmation_screen()
                    continue
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.__state = PLAY
                        continue
                    if event.key == pygame.K_q:
                        self.__render_quit_menu_confirmation_screen()
                        continue
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.__play_click_sound()
                    if info_button_rect.collidepoint(event.pos):
                        self.__state = INSTRUCTIONS
                        continue
                    if play_button_rect.collidepoint(event.pos):
                        self.__state = PLAY
                        continue
                    if quit_button_rect.collidepoint(event.pos):
                        self.__render_quit_menu_confirmation_screen()
                        continue

            # We fill the background
            self.__canvas.fill(BLACK)    
            # We paint ui components
            self.__canvas.blit(self.__bg_texture, self.__bg_rect)
            self.__canvas.blit(self.__mm_title_bg_texture, mm_title_bg_rect)
            self.__canvas.blit(self.__button_play_texture, play_button_rect)
            self.__canvas.blit(self.__button_info_texture, info_button_rect)
            self.__canvas.blit(self.__button_quit_texture, quit_button_rect)
            self.__canvas.blit(title_text, (164, 20))
            self.__canvas.blit(play_button_text, (SCREEN_WIDTH / 2 - 30, SCREEN_HEIGHT / 2 - 115))
            self.__canvas.blit(info_button_text, (SCREEN_WIDTH / 2 - 80, SCREEN_HEIGHT / 2 - 35))
            self.__canvas.blit(quit_button_text, (SCREEN_WIDTH / 2 - 30, SCREEN_HEIGHT / 2 + 50))

            self.__update_cursor()

            pygame.display.flip()
            return

    def __render_info_screen(self):
        """ Renders info screen """

        self.__bg_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        
        interface_rect = self.__info_bg_texture.get_rect()
        title_text = self.__font_lg.render("THE SNAKE", True, WHITE)

        button_back_rect = self.__button_back_texture.get_rect()

        interface_rect.topleft = (0, 0)
        button_back_rect.topleft = (SCREEN_WIDTH - 206, SCREEN_HEIGHT - 78)
        
        info_line_1 = self.__font_md.render("- Do not touch the edges of the playing area", True, WHITE)
        info_line_2 = self.__font_md.render("- Eat all the apples you can", True, WHITE)
        info_line_3 = self.__font_md.render("- Don't bite yourself!", True, WHITE)
        info_line_4 = self.__font_md.render("- Have fun playing with this nice snake...", True, WHITE)
        
        back_button_text = self.__font_md.render("BACK", True, WHITE)

        # We execute this screen while 'state' is = INSTRUCTIONS
        while self.__state == INSTRUCTIONS:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__render_quit_menu_confirmation_screen()
                    continue
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.__play_click_sound()
                    if button_back_rect.collidepoint(event.pos):
                        self.__state = MENU
                        continue
                    
            self.__canvas.fill(BLACK)
            self.__canvas.blit(self.__bg_texture, self.__bg_rect)
            self.__canvas.blit(self.__info_bg_texture, interface_rect)
            self.__canvas.blit(title_text, (164, 20))
            self.__canvas.blit(info_line_1, (70, 200))
            self.__canvas.blit(info_line_2, (70, 230))
            self.__canvas.blit(info_line_3, (70, 260))
            self.__canvas.blit(info_line_4, (70, 290))

            self.__canvas.blit(self.__button_back_texture, button_back_rect)
            self.__canvas.blit(back_button_text, (SCREEN_WIDTH - 120, SCREEN_HEIGHT - 62))
            
            self.__update_cursor()
            pygame.display.flip()

    def __convert_pos_to_coords(self, pos) -> tuple:
        """ Convert grid position to screen coordinates within the snake's movement zone """
        if not (isinstance(pos, tuple) and len(pos) == 2):
            raise ValueError
        pos_x = pos[0]
        pos_y = pos[1]
        
        if (
            pos_x < 0 or pos_x >= GRID_CELLS or
            pos_y < 0 or pos_y >= GRID_CELLS
            ):
            raise IndexError

        # Returns the coordinates of the upper left corner of the corresponding grid on the map
        return (MIN_X + pos_x * CELL_SIZE, MIN_Y + pos_y * CELL_SIZE)

    def __convert_coords_to_pos(self, coords) -> tuple:
        """ Converts screen coordinates within the snake's movement zone to position on the grid """
        if not (isinstance(coords, tuple) and len(coords) == 2):
            raise ValueError

        coords_x = coords[0] - MIN_X
        coords_y = coords[1] - MIN_Y
        
        if (
            coords_x < 0 or coords_x >= SCREEN_WIDTH - MIN_X or
            coords_y < 0 or coords_y >= SCREEN_HEIGHT - MIN_Y
            ):
            raise IndexError
        
        # Returns the position of the grid in which the indicated coordinates are found
        return (coords_x // CELL_SIZE, coords_y // CELL_SIZE)

    def __render_snake(self, snake_body_list):
        """ Renders the snake """
        # Draw snake head
        head = pygame.transform.rotate(self.__snake_head_sprite, snake_body_list[-1][1] * -90)
        head_rect = snake_body_list[-1][0]
        self.__canvas.blit(head, head_rect)

        # We draw snake body
        for XnY in range(1, len(snake_body_list) - 1):
            dir = snake_body_list[XnY][1]
            # We found curves
            if (snake_body_list[XnY+1][1] != dir):
                # NOTA: can it optimize?
                if (dir == UP):
                    if (snake_body_list[XnY+1][1] == RIGHT):
                        rot = -1 #
                    else:
                        rot = 0
                elif (dir == LEFT):
                    if (snake_body_list[XnY+1][1] == UP):
                        rot = 2
                    else:
                        rot = -1
                elif (dir == RIGHT):
                    if (snake_body_list[XnY+1][1] == UP):
                        rot = 1
                    else:
                        rot = 0
                else:
                    if (snake_body_list[XnY+1][1] == RIGHT):
                        rot = 2
                    else:
                        rot = 1

                body = pygame.transform.rotate(self.__snake_curved_body_sprite, rot * -90)
            else:
                body = pygame.transform.rotate(self.__snake_body_sprite, snake_body_list[XnY][1] * -90)

            body_rect = snake_body_list[XnY][0]
            self.__canvas.blit(body, body_rect)

        # Lastly we draw the tail
        dir = snake_body_list[1][1]
        tail = pygame.transform.rotate(self.__snake_tail_sprite, dir * -90)
        tail_rect = snake_body_list[0][0]    
        self.__canvas.blit(tail, tail_rect)

    def __spawn_apple(self):
        """ Spawns a new apple in the map """
        apple_x = random.randint(MIN_X, MAX_X - CELL_SIZE)
        apple_y = random.randint(MIN_Y, MAX_Y - CELL_SIZE)    

        apple_x, apple_y = self.__convert_pos_to_coords(self.__convert_coords_to_pos((apple_x, apple_y)))
        apple_rect = pygame.Rect(apple_x, apple_y, CELL_SIZE, CELL_SIZE)

        # TODO: check if the spawn position is bussy 
        # if (apple_rect.colliderect(loquesea)):
        # return spawn_apple()

        return (apple_x, apple_y)

    def __render_level_bar(self, progress):
        """ Draw the level progress bar in the game interface """
        n = progress * 4 # each progress point is 4 pixel length
        
        for i in range(0, n):
            if (i >= 62):
                img = self.__level_bar_end_texture
            elif (i < 2 or i > 60):
                img = self.__level_bar_start_texture
            else:
                img = self.__level_bar_texture
            self.__canvas.blit(img, (181 + i, 27))


    def __render_health_bar(self, health):
        """ Draw the health bar in the game interface """
        n = health * 4 # each health point is 4 pixel length
        
        # Max 16 health points
        for i in range(0, n):
            if (i >= 62):
                img = self.__health_bar_end
            elif (i < 2 or i > 60):
                img = self.__health_bar_start
            else:
                img = self.__health_bar
            self.__canvas.blit(img, (181 + i, 59))

    def __render_pause_menu(self):
        """ Renders pause screen"""
        # The pause menu only appears during the game and without interrupting its execution. we just draw it
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.set_alpha(150)
        interface_rect = self.__pause_interface_texture.get_rect()
        interface_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT/2)
        
        
        pause_text_1 = self.__font_md.render("GAME PAUSED", True, WHITE)
        pause_text_2 = self.__font_md.render("Press 'Q' to back to the main menu", True, WHITE)
        pause_text_3 = self.__font_md.render("or press 'C' to resume the game", True, WHITE)

        self.__canvas.blit(overlay, (0, 0))
        self.__canvas.blit(self.__pause_interface_texture, interface_rect)
        self.__canvas.blit(pause_text_1, (230, 220))
        self.__canvas.blit(pause_text_2, (120, 280))
        self.__canvas.blit(pause_text_3, (140, 320))
        return

    def __render_game_over_interface(self):
        """ Renders game over screen"""

        interface_rect = self.__go_interface_texture.get_rect()
        interface_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT/2)
        
        # Gets buttons rectangles
        new_play_button = pygame.Rect(SCREEN_WIDTH / 2 - 131, SCREEN_HEIGHT / 2 - 96, 252 , 42)
        quit_button     = pygame.Rect(SCREEN_WIDTH / 2 - 118, SCREEN_HEIGHT / 2 + 52, 223 , 42)
        
        play_button_text = self.__font_md.render("PLAY AGAIN", True, WHITE)
        quit_button_text = self.__font_md.render("QUIT TO MENU", True, WHITE)

        # We execute this screen while 'state' is = INSTRUCTIONS
        while self.__state == GAME_OVER:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__render_quit_menu_confirmation_screen()
                    continue
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.__play_click_sound()
                    if new_play_button.collidepoint(event.pos):                    
                        self.__state = PLAY
                        break
                    # Salmos al menú
                    if quit_button.collidepoint(event.pos):
                        self.__state = MENU
                        break
            self.__canvas.fill(BLACK)
            self.__canvas.blit(self.__go_interface_texture, interface_rect)
            self.__canvas.blit(play_button_text, (220, 210))
            self.__canvas.blit(quit_button_text, (190, 354))

            self.__update_cursor()
            pygame.display.flip()
        return

    def __play_eating_sound(self):
        """ Plays the sound when the snake eats an object """
        pygame.mixer.Channel(1).play(self.__snake_eat_sound, maxtime=2000) # Just reproduce first 2 seconds.
        return

    def __play_level_up_sound(self):
        """ Plays level up sound """
        pygame.mixer.Channel(2).play(self.__level_up_sound)
        return

    def __render_play_screen(self):
        """ Renders game screen """

        interface_rect = self.__game_interface_texture.get_rect()

        boton_pausa = pygame.Rect(546, 28, 40, 48)

        # Sets initial level
        current_level = LEVEL

        # Initial coordinates of the head (On the screen)
        snake_head_x = MIN_X + CELL_SIZE * 2
        snake_head_y = MIN_Y
        # Starting head position (On the game map)
        pos_x, pos_y = self.__convert_coords_to_pos((snake_head_x, snake_head_y))

        # Snake starting direction
        direction = RIGHT
        snake_head_rect = pygame.Rect(snake_head_x, snake_head_y, CELL_SIZE, CELL_SIZE)
        # Definición inicial de las partes de la serpiente
        snake_body_list = [
            (pygame.Rect(snake_head_x - CELL_SIZE * 2, snake_head_y, CELL_SIZE, CELL_SIZE), direction), # tail
            (pygame.Rect(snake_head_x - CELL_SIZE, snake_head_y, CELL_SIZE, CELL_SIZE), direction), # body
            (snake_head_rect, direction) # head
        ]

        # Keyboard delay control
        keyboard_delay_timer = 0

        # We spawn first apple
        apple_x, apple_y = self.__spawn_apple()
        # Overall Match Score
        score = 0
        # Snake length, to control the size of the snake more quickly.
        snake_lenght = 3

        # % of progress in the current level
        level_progress = 0

        # Snake movement speed
        current_snake_speed = INITIAL_SPEED
        current_snake_health = 16

        # We keep running the game while game state = PLAY or PAUSED
        while self.__state == PLAY or self.__state == PAUSED:
            # Delay attempt on keyboard input to avoid weird effects on snake movement
            if (keyboard_delay_timer != 0):
                keyboard_delay_timer += 1
                if (keyboard_delay_timer > 10): # delay of 10 game ticks
                    keyboard_delay_timer = 0

            # Process input events
            for event in pygame.event.get():
                # Clossing window
                if event.type == pygame.QUIT:
                    self.__render_quit_menu_confirmation_screen()
                # Keyboard events
                if event.type == pygame.KEYDOWN and keyboard_delay_timer == 0:
                    if (self.__state == PAUSED):
                        if (event.key == pygame.K_q):
                            self.__render_quit_menu_confirmation_screen()
                        elif (event.key == pygame.K_c):
                            self.__state = PLAY
                        # If the game is paused, the other keys do not perform any action.
                        continue
                    # Direction keys
                    if event.key == pygame.K_LEFT:
                        if direction == RIGHT:
                            pass
                        else:
                            direction = LEFT
                        keyboard_delay_timer = 1
                    elif event.key == pygame.K_RIGHT:
                        if direction == LEFT:
                            pass
                        else:
                            direction = RIGHT
                        keyboard_delay_timer = 1
                    elif event.key == pygame.K_UP:
                        if direction == DOWN:
                            pass
                        else:
                            direction = UP
                        keyboard_delay_timer = 1
                    elif event.key == pygame.K_DOWN:
                        if direction == UP:
                            pass
                        else:
                            direction = DOWN
                        keyboard_delay_timer = 1
                # Mouse events
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # If the game is paused, the mouse has no function here.
                    if (self.__state == PAUSED):
                        continue
                    # Click on the pause button
                    if boton_pausa.collidepoint(event.pos):
                        self.__play_click_sound()
                        self.__state = PAUSED
                        break

            # Game logic is only updated if the game is not paused.
            if (self.__state != PAUSED):
                # We move the position of the head in the indicated direction
                if direction == UP:
                    snake_head_y -= CELL_SIZE * current_snake_speed
                elif direction == DOWN:
                    snake_head_y += CELL_SIZE * current_snake_speed
                elif direction == RIGHT:
                    snake_head_x += CELL_SIZE * current_snake_speed
                elif direction == LEFT:
                    snake_head_x -= CELL_SIZE * current_snake_speed

                # If the head touches any of the side walls, game over!!.
                if (snake_head_x < MIN_X or snake_head_x >= MAX_X or snake_head_y < MIN_Y or snake_head_y >= MAX_Y):
                    self.__state = GAME_OVER
                    break

                # We convert the coordinates of the screen in position on the map and move the head if it corresponds
                siguiente_pos_x, siguiente_pos_y = self.__convert_coords_to_pos((snake_head_x, snake_head_y))
                # If the position of the head on the map has changed, we insert the new position on the snake.
                if (pos_x != siguiente_pos_x or pos_y != siguiente_pos_y):
                    pos_x = siguiente_pos_x
                    pos_y = siguiente_pos_y
                    keyboard_delay_timer = 0
                    cx, cy = self.__convert_pos_to_coords((pos_x, pos_y))
                    # We update the position of the head
                    snake_head_rect = pygame.Rect(cx, cy, CELL_SIZE, CELL_SIZE)
                    snake_body_list.append((snake_head_rect, direction))
                else:
                    # Otherwise, we simply get the position of the snake's head to make it easier to check for collisions later.
                    snake_head_rect = snake_body_list[-1][0]

                # We eliminate the 'tail' of the snake in case of advancing or decreasing its length for any reason
                if len(snake_body_list) > snake_lenght:
                    del snake_body_list[0]

                # We check if the snake bites itself and if so, it dies!!
                for parte in snake_body_list[:-1]:
                    if snake_head_rect.colliderect(parte[0]):
                        self.__state = GAME_OVER
                        break

                # We check if the head collides with the apple and if so, we apply the effect
                apple_rect = pygame.Rect(apple_x, apple_y, CELL_SIZE, CELL_SIZE)
                apple_rect.topleft = (apple_x, apple_y)

                # The snake eats an object on the map
                if snake_head_rect.colliderect(apple_rect):
                    self.__play_eating_sound()
                    apple_x, apple_y = self.__spawn_apple()
                    snake_lenght += 1
                    score += 1
                    level_progress += 1
                    apple_rect = pygame.Rect(apple_x, apple_y, CELL_SIZE, CELL_SIZE)
                    apple_rect.topleft = (apple_x, apple_y)

                # We reached the score for the next level
                if (level_progress >= 16):
                    level_progress = 0
                    current_level += 1
                    current_snake_speed *= 1.5 # We increase the speed

                    # TODO: Optimize the transition between levels
                    self.__play_level_up_sound()
            
            # We fill the background
            self.__canvas.fill(BLACK)
            self.__canvas.blit(self.__game_interface_texture, interface_rect)


            score_text = self.__font_sm.render("SCORE: {}".format(score), True, WHITE)
            score_text_rect = score_text.get_rect()
            score_text_rect.topleft = (28, 24)

            level_text = self.__font_sm.render("LEVEL: {}".format(current_level), True, WHITE)
            level_text_rect = level_text.get_rect()
            level_text_rect.topleft = (28, 52)
            
            self.__canvas.blit(score_text, score_text_rect)
            self.__canvas.blit(score_text, score_text_rect)
            self.__canvas.blit(level_text, level_text_rect)

            # We update the progress in the interface
            self.__render_level_bar(level_progress)
            self.__render_health_bar(current_snake_health)

            # We render the snake
            self.__render_snake(snake_body_list)
            # We render the apple
            self.__canvas.blit(self.__red_apple_texture, apple_rect)
            
            if self.__state == PAUSED:
                self.__render_pause_menu()
            
            self.__update_cursor()
            pygame.display.flip()
            self.__clock.tick(FPS)

    # Here should go the handling of input events (mouse, keyboard...)
    def __process_input(self):
        pass

    # This is where the logic of the game should go
    def __game_update(self):
        pass

    # Here should go the update of the screen images
    def __render_screen(self):
        pass

    # Game start and main screen loop
    def run_game(self):

    # sounds
        try:
            music_file = path.join(PATH, 'res', 'music', 'musica.mp3')
            if path.isfile(music_file):
                music = pygame.mixer.music.load(music_file)
                pygame.mixer.music.play(loops=-1)
                pygame.mixer.music.set_volume(.5)
        except:
            pass

        while self.__running:
            self.__process_input()
            self.__game_update()
            self.__render_screen()
            if self.__state == MENU:
                self.__render_main_menu_screen()
            elif self.__state == PLAY or self.__state == PAUSED:
                self.__render_play_screen()
            elif self.__state == INSTRUCTIONS:
                self.__render_info_screen()
            elif self.__state == GAME_OVER:
                self.__render_game_over_interface()
            else:
                self.__running = False

game = Game()
game.run_game()

pygame.quit()
sys.exit()
