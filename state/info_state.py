from os.path import join
from typing import List

from constants import (BLACK, INSTRUCTIONS, MENU, PATH, SCREEN_HEIGHT,
                       SCREEN_WIDTH)
from graphics.screen import Screen
from pygame import MOUSEBUTTONDOWN
from pygame.event import Event
from pygame.image import load
from pygame.transform import scale

from state.game_state import GameState


class InfoState(GameState):
    """ Renders info screen """
    
    _status = INSTRUCTIONS
    
    def __init__(self, game) -> None:
        super().__init__(game)
        self._load_resources()        
    
    def _load_resources(self) -> None:
        
        self.__bg_texture = scale(load(join(PATH, "res", 'images', "bg.png")), (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.__bg_rect = self.__bg_texture.get_rect()
        self.__bg_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        
        self.__info_bg_texture  = load(join(PATH, 'res', 'images', 'info_interface.png'))
        self.__interface_rect = self.__info_bg_texture.get_rect()
        self.__title_text = "THE SNAKE"

        self.__button_back_texture = load(join(PATH, 'res', 'images', 'buttons', 'button_back.png'))
        self.__button_back_rect = self.__button_back_texture.get_rect()

        self.__interface_rect.topleft = (0, 0)
        self.__button_back_rect.topleft = (SCREEN_WIDTH - 206, SCREEN_HEIGHT - 78)
        
    def get_status(self) -> int:
        return self._status

    def update(self, time: int) -> None:
        pass
    
    def process_input(self, input: List[Event]) -> None:
        for event in input:
            if event.type == MOUSEBUTTONDOWN:
                self._game.get_sound_manager().play_click_sound()
                if self.__button_back_rect.collidepoint(event.pos):
                    self._game.set_status(MENU)
                    return
    
    def render(self, screen: Screen) -> None:        
        screen.fill(BLACK)
        screen.blit(self.__bg_texture, self.__bg_rect)
        screen.blit(self.__info_bg_texture, self.__interface_rect)
        screen.draw_string(self.__title_text, (250, 30))
        screen.draw_string("- Do not touch the edges of the playing area", (70, 200))
        screen.draw_string("- Eat all the apples you can", (70, 230))
        screen.draw_string("- Don't bite yourself!", (70, 260))
        screen.draw_string("- Have fun playing with this nice snake...", (70, 290))

        screen.blit(self.__button_back_texture, self.__button_back_rect)
        screen.draw_string("BACK", (SCREEN_WIDTH - 120, SCREEN_HEIGHT - 62))
