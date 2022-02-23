from os.path import join
from typing import List

from constants import (BLACK, GAME_OVER, MENU, PATH, PLAY, SCREEN_HEIGHT,
                       SCREEN_WIDTH)
from graphics.screen import Screen
from pygame import MOUSEBUTTONDOWN, Rect
from pygame.event import Event
from pygame.image import load

from state.game_state import GameState


class GameOverState(GameState):
    
    __state = GAME_OVER
    
    def __init__(self, game) -> None:
        super().__init__(game)
        self._load_resources()
        
    def get_status(self) -> int:
        return self.__state
        
    def _load_resources(self) -> None:        
        self.__go_interface_texture  = load(join(PATH, 'res', 'images', 'game_over_interface.png'))
        self.__interface_rect = self.__go_interface_texture.get_rect()
        self.__interface_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT/2)
        
        # Gets buttons rectangles
        self.__new_play_button = Rect(SCREEN_WIDTH / 2 - 131, SCREEN_HEIGHT / 2 - 96, 252 , 42)
        self.__quit_button     = Rect(SCREEN_WIDTH / 2 - 118, SCREEN_HEIGHT / 2 + 52, 223 , 42)
    
    def update(self, time: int) -> None:
        pass
    
    def process_input(self, input: List[Event]) -> None:
        for event in input:
            if event.type == MOUSEBUTTONDOWN:
                if self.__new_play_button.collidepoint(event.pos):                    
                    self._game.get_sound_manager().play_click_sound()
                    self._game.set_status(PLAY)
                    return
                # We back to main manu
                if self.__quit_button.collidepoint(event.pos):
                    self._game.get_sound_manager().play_click_sound()
                    self._game.set_status(MENU)
                    return
    
    def render(self, screen: Screen) -> None:        
        screen.fill(BLACK)
        screen.blit(self.__go_interface_texture, self.__interface_rect)
        screen.draw_string("PLAY AGAIN", (220, 210))
        screen.draw_string("QUIT TO MENU", (190, 354))
