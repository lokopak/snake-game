from os.path import join
from random import randint
from typing import List, Tuple

from constants import (BLACK, CELL_SIZE, DOWN, GAME_OVER, GRID_CELLS,
                       INITIAL_SPEED, LEFT, LEVEL, MAX_X, MAX_Y, MIN_X, MIN_Y,
                       PATH, PAUSED, PLAY, RIGHT, SCREEN_HEIGHT, SCREEN_WIDTH,
                       UP)
from graphics.screen import Screen
from pygame import (K_DOWN, K_LEFT, K_RIGHT, K_UP, KEYUP, MOUSEBUTTONDOWN,
                    SRCALPHA, K_c, K_q, Rect, Surface)
from pygame.event import Event
from pygame.image import load
from pygame.transform import rotate, scale

from state.game_state import GameState


class PlayState(GameState):
    
    _status = PLAY
    __state = PLAY
    
    def __init__(self, game) -> None:
        super().__init__(game)
        self.__screen = game.get_screen()
        self._load_resources()
        self._init_level()
        
    def _load_resources(self) -> None:
        """ Renders game screen """

        # Preload game interface textures.
        self.__pause_interface_texture  = load(join(PATH, 'res', 'images', 'pause_interface.png'))
        self.__game_interface_texture  = load(join(PATH, 'res', 'images', 'game_interface.png'))

        self.__level_bar_start_texture = load(join(PATH, 'res', 'images', 'level_bar_start.png'))
        self.__level_bar_texture = load(join(PATH, 'res', 'images', 'level_bar.png'))
        self.__level_bar_end_texture = load(join(PATH, 'res', 'images', 'level_bar_end.png'))
        self.__health_bar_start = load(join(PATH, 'res', 'images', 'health_bar_start.png'))
        self.__health_bar = load(join(PATH, 'res', 'images', 'health_bar.png'))
        self.__health_bar_end = load(join(PATH, 'res', 'images', 'health_bar_end.png'))

        # Preload snake sprites. They should load at the beginning of the game
        self.__snake_head_sprite = scale(load(join(PATH, 'res', 'images', 'snake_head.png')), (CELL_SIZE, CELL_SIZE))
        self.__snake_body_sprite = scale(load(join(PATH, 'res', 'images', 'snake_body.png')), (CELL_SIZE, CELL_SIZE))
        self.__snake_curved_body_sprite = scale(load(join(PATH, 'res', 'images', 'snake_curved_body.png')), (CELL_SIZE, CELL_SIZE))
        self.__snake_tail_sprite = scale(load(join(PATH, 'res', 'images', 'snake_tile.png')), (CELL_SIZE, CELL_SIZE))

        # Preload apple sprite
        self.__red_apple_texture = scale(load(join(PATH, 'res', 'images', 'red_apple.png')), (CELL_SIZE, CELL_SIZE))
        self.__red_apple_rect = self.__red_apple_texture.get_rect()
        
        self.__interface_rect = self.__game_interface_texture.get_rect()
        self.__boton_pausa = Rect(546, 28, 40, 48)
        
    def get_status(self) -> int:
        return self._status
    
    def _init_level(self) -> None:
        # Sets initial level
        self.__current_level = LEVEL

        # Initial coordinates of the head (On the screen)
        self.__snake_head_x = MIN_X + CELL_SIZE * 2
        self.__snake_head_y = MIN_Y
        
        # Starting head position (On the game map)
        self.__pos_x, self.__pos_y = self.__convert_coords_to_pos((self.__snake_head_x, self.__snake_head_y))

        # Snake starting direction
        self.__direction = RIGHT
        
        snake_head_rect = Rect(self.__snake_head_x, self.__snake_head_y, CELL_SIZE, CELL_SIZE)
        # Definición inicial de las partes de la serpiente
        self.__snake_body_list = [
            (Rect(self.__snake_head_x - CELL_SIZE * 2, self.__snake_head_y, CELL_SIZE, CELL_SIZE), self.__direction), # tail
            (Rect(self.__snake_head_x - CELL_SIZE, self.__snake_head_y, CELL_SIZE, CELL_SIZE), self.__direction), # body
            (snake_head_rect, self.__direction) # head
        ]

        # Keyboard delay control
        self.__keyboard_delay_timer = 0

        # We spawn first apple
        self.__apple_x, self.__apple_y = self.__spawn_apple()
        # Overall Match Score
        self.__score = 0
        # Snake length, to control the size of the snake more quickly.
        self.__snake_lenght = 3

        # % of progress in the current level
        self.__level_progress = 0

        # Snake movement speed
        self.__current_snake_speed = INITIAL_SPEED
        self.__current_snake_health = 16
    
    def process_input(self, input: List[Event]) -> None:
        # Delay attempt on keyboard input to avoid weird effects on snake movement
        if (self.__keyboard_delay_timer != 0):
            self.__keyboard_delay_timer += 1
            if (self.__keyboard_delay_timer > 10): # delay of 10 game ticks
                self.__keyboard_delay_timer = 0

        # Process input events
        for event in input:
            # Keyboard events
            if event.type == KEYUP and self.__keyboard_delay_timer == 0:
                if (self.__state == PAUSED):
                    if (event.key == K_q):
                        self._game.quit()
                    elif (event.key == K_c):
                        self.__state = PLAY
                    # If the game is paused, the other keys do not perform any action.
                    continue
                # Direction keys
                if event.key == K_LEFT:
                    if self.__direction == RIGHT:
                        pass
                    else:
                        self.__direction = LEFT
                    self.__keyboard_delay_timer = 1
                elif event.key == K_RIGHT:
                    if self.__direction == LEFT:
                        pass
                    else:
                        self.__direction = RIGHT
                    self.__keyboard_delay_timer = 1
                elif event.key == K_UP:
                    if self.__direction == DOWN:
                        pass
                    else:
                        self.__direction = UP
                    self.__keyboard_delay_timer = 1
                elif event.key == K_DOWN:
                    if self.__direction == UP:
                        pass
                    else:
                        self.__direction = DOWN
                    self.__keyboard_delay_timer = 1
            # Mouse events
            if event.type == MOUSEBUTTONDOWN:
                # If the game is paused, the mouse has no function here.
                if (self.__state == PAUSED):
                    continue
                # Click on the pause button
                if self.__boton_pausa.collidepoint(event.pos):
                    self._game.get_sound_manager().play_click_sound()
                    self.__state = PAUSED
                    break
    
    def update(self, time: int) -> None:
        # Game logic is only updated if the game is not paused.
        if (self.__state != PAUSED):
            # We move the position of the head in the indicated direction
            if self.__direction == UP:
                self.__snake_head_y -= CELL_SIZE * self.__current_snake_speed
            elif self.__direction == DOWN:
                self.__snake_head_y += CELL_SIZE * self.__current_snake_speed
            elif self.__direction == RIGHT:
                self.__snake_head_x += CELL_SIZE * self.__current_snake_speed
            elif self.__direction == LEFT:
                self.__snake_head_x -= CELL_SIZE * self.__current_snake_speed

            # If the head touches any of the side walls, game over!!.
            if (self.__snake_head_x < MIN_X or self.__snake_head_x >= MAX_X or self.__snake_head_y < MIN_Y or self.__snake_head_y >= MAX_Y):
                self._game.set_status(GAME_OVER)
                return

            # We convert the coordinates of the screen in position on the map and move the head if it corresponds
            siguiente_pos_x, siguiente_pos_y = self.__convert_coords_to_pos((self.__snake_head_x, self.__snake_head_y))
            # If the position of the head on the map has changed, we insert the new position on the snake.
            if (self.__pos_x != siguiente_pos_x or self.__pos_y != siguiente_pos_y):
                self.__pos_x = siguiente_pos_x
                self.__pos_y = siguiente_pos_y
                self.__keyboard_delay_timer = 0
                cx, cy = self.__convert_pos_to_coords((self.__pos_x, self.__pos_y))
                # We update the position of the head
                snake_head_rect = Rect(cx, cy, CELL_SIZE, CELL_SIZE)
                self.__snake_body_list.append((snake_head_rect, self.__direction))
            else:
                # Otherwise, we simply get the position of the snake's head to make it easier to check for collisions later.
                snake_head_rect = self.__snake_body_list[-1][0]

            # We eliminate the 'tail' of the snake in case of advancing or decreasing its length for any reason
            if len(self.__snake_body_list) > self.__snake_lenght:
                del self.__snake_body_list[0]

            # We check if the snake bites itself and if so, it dies!!
            for parte in self.__snake_body_list[:-1]:
                if snake_head_rect.colliderect(parte[0]):
                    self._game.set_status(GAME_OVER)
                    return

            # We check if the head collides with the apple and if so, we apply the effect
            self.__apple_rect = Rect(self.__apple_x, self.__apple_y, CELL_SIZE, CELL_SIZE)
            self.__apple_rect.topleft = (self.__apple_x, self.__apple_y)

            # The snake eats an object on the map
            if snake_head_rect.colliderect(self.__apple_rect):
                self._game.get_sound_manager().play_eating_sound()
                self.__apple_x, self.__apple_y = self.__spawn_apple()
                self.__snake_lenght += 1
                self.__score += 1
                self.__level_progress += 1
                self.__apple_rect = Rect(self.__apple_x, self.__apple_y, CELL_SIZE, CELL_SIZE)
                self.__apple_rect.topleft = (self.__apple_x, self.__apple_y)

            # We reached the score for the next level
            if (self.__level_progress >= 1):
                self.__level_progress = 0
                self.__current_level += 1
                self.__current_snake_speed *= 1.2 # We increase the speed
                # TODO: Optimize the transition between levels
                self._game.get_sound_manager().play_level_up_sound()
    
    def render(self, screen: Screen) -> None:            
            # We fill the background
            self.__screen.fill(BLACK)
            self.__screen.blit(self.__game_interface_texture, self.__interface_rect)
            
            self.__screen.draw_string("SCORE: {}".format(self.__score), (28, 20))
            self.__screen.draw_string("LEVEL: {}".format(self.__current_level), (28, 48))

            # We update the progress in the interface
            self.__render_level_bar(self.__level_progress)
            self.__render_health_bar(self.__current_snake_health)

            # We render the snake
            self.__render_snake(self.__snake_body_list)
            # We render the apple
            self.__screen.blit(self.__red_apple_texture, self.__apple_rect)
            
            if self.__state == PAUSED:
                self.__render_pause_menu()

    def __convert_pos_to_coords(self, pos) -> Tuple[float, float]:
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

    def __convert_coords_to_pos(self, coords: Tuple[float, float]) -> Tuple[int, int]:
        """ Converts screen coordinates within the snake's movement zone to position on the grid """

        coords_x = coords[0] - MIN_X
        coords_y = coords[1] - MIN_Y
        
        if (
            coords_x < 0 or coords_x >= SCREEN_WIDTH - MIN_X or
            coords_y < 0 or coords_y >= SCREEN_HEIGHT - MIN_Y
            ):
            raise IndexError
        
        # Returns the position of the grid in which the indicated coordinates are found
        return (coords_x // CELL_SIZE, coords_y // CELL_SIZE)
    
    def __render_snake(self, snake_body_list: List) -> None:
        """ Renders the snake """
        # Draw snake head
        head = rotate(self.__snake_head_sprite, snake_body_list[-1][1] * -90)
        head_rect = snake_body_list[-1][0]
        self.__screen.blit(head, head_rect)

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

                body = rotate(self.__snake_curved_body_sprite, rot * -90)
            else:
                body = rotate(self.__snake_body_sprite, snake_body_list[XnY][1] * -90)

            body_rect = snake_body_list[XnY][0]
            self.__screen.blit(body, body_rect)

        # Lastly we draw the tail
        dir = snake_body_list[1][1]
        tail = rotate(self.__snake_tail_sprite, dir * -90)
        tail_rect = snake_body_list[0][0]    
        self.__screen.blit(tail, tail_rect)

    def __spawn_apple(self) -> None:
        """ Spawns a new apple in the map """
        apple_x = randint(MIN_X, MAX_X - CELL_SIZE)
        apple_y = randint(MIN_Y, MAX_Y - CELL_SIZE)    

        apple_x, apple_y = self.__convert_pos_to_coords(self.__convert_coords_to_pos((apple_x, apple_y)))
        apple_rect = Rect(apple_x, apple_y, CELL_SIZE, CELL_SIZE)

        # TODO: check if the spawn position is bussy 
        # if (apple_rect.colliderect(loquesea)):
        # return spawn_apple()

        return (apple_x, apple_y)

    def __render_level_bar(self, progress: int) -> None:
        """ Draw the level progress bar in the game interface """
        n = progress * 4 # each progress point is 4 pixel length
        
        for i in range(0, n):
            if (i >= 62):
                img = self.__level_bar_end_texture
            elif (i < 2 or i > 60):
                img = self.__level_bar_start_texture
            else:
                img = self.__level_bar_texture
            self.__screen.blit(img, (181 + i, 27))


    def __render_health_bar(self, health: int) -> None:
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
            self.__screen.blit(img, (181 + i, 59))

    def __render_pause_menu(self) -> None:
        """ Renders pause screen"""
        # The pause menu only appears during the game and without interrupting its execution. we just draw it
        overlay = Surface((SCREEN_WIDTH, SCREEN_HEIGHT), SRCALPHA)
        overlay.set_alpha(150)
        interface_rect = self.__pause_interface_texture.get_rect()
        interface_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT/2)

        self.__screen.blit(overlay, (0, 0))
        self.__screen.blit(self.__pause_interface_texture, interface_rect)
        self.__screen.draw_string("GAME PAUSED", (230, 220))
        self.__screen.draw_string("Press 'Q' to back to the main menu", (120, 280))
        self.__screen.draw_string("or press 'C' to resume the game", (140, 320))
        return
