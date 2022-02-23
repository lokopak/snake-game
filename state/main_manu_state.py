from os.path import join

from constants import (BLACK, INSTRUCTIONS, MENU, PATH, PLAY, SCREEN_HEIGHT,
                       SCREEN_WIDTH)
from graphics.screen import Screen
from pygame import KEYUP, MOUSEBUTTONDOWN, K_p, K_q
from pygame.image import load
from pygame.transform import scale

from state.game_state import GameState
from state.quit_menu_state import QuitMenuState


class MainMenuState(GameState):
    
    _status = MENU
    
    def __init__(self, game) -> None:
        super().__init__(game)
        self._load_resources()

    def _load_resources(self) -> None:
        self.__bg_texture = load(join(PATH, "res", 'images', "bg.png"))
        self.__bg_texture = scale(self.__bg_texture, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.__bg_rect = self.__bg_texture.get_rect()
        
        self.__mm_title_bg_texture = load(join(PATH, 'res', 'images', 'main_menu_title_bg.png'))
        self.__button_play_texture = load(join(PATH, 'res', 'images', 'buttons', 'button_play.png'))
        self.__button_info_texture  = load(join(PATH, 'res', 'images', 'buttons', 'button_info.png'))
        self.__button_quit_texture = load(join(PATH, 'res', 'images', 'buttons', 'button_quit.png'))
        
        # Gets button rectangles
        self.__mm_title_bg_rect = self.__mm_title_bg_texture.get_rect()
        self.__play_button_rect = self.__button_play_texture.get_rect()
        self.__info_button_rect = self.__button_info_texture.get_rect()
        self.__quit_button_rect = self.__button_quit_texture.get_rect()

        # We define the positions of each component of the screen
        self.__bg_rect.center   = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.__mm_title_bg_rect.center = (SCREEN_WIDTH / 2, 50)
        self.__play_button_rect.center = (SCREEN_WIDTH / 2 - 20, SCREEN_HEIGHT / 2 - 98)
        self.__info_button_rect.center = (SCREEN_WIDTH / 2 - 22, SCREEN_HEIGHT / 2 - 18)
        self.__quit_button_rect.center = (SCREEN_WIDTH / 2 - 20, SCREEN_HEIGHT / 2 + 67)
        
    def get_status(self) -> int:
        return self._status

    def process_input(self, input) -> None:
        for event in input:
            if event.type == KEYUP:
                if event.key == K_p:
                    self._game.set_status(PLAY)
                    return
                if event.key == K_q:
                    self._game.quit()
                    return
            if event.type == MOUSEBUTTONDOWN:
                if self.__info_button_rect.collidepoint(event.pos):
                    self._game.get_sound_manager().play_click_sound()
                    self._game.set_status(INSTRUCTIONS)
                    return
                if self.__play_button_rect.collidepoint(event.pos):
                    self._game.get_sound_manager().play_click_sound()
                    self._game.set_status(PLAY)
                    return
                if self.__quit_button_rect.collidepoint(event.pos):
                    self._game.get_sound_manager().play_click_sound()
                    self._game.quit()
                    return

    def update(self, time: int) -> None:
        pass
    
    def render(self, screen: Screen) -> None:
        # We fill the background
        screen.fill(BLACK)    
        # We paint ui components
        screen.blit(self.__bg_texture, self.__bg_rect)
        screen.blit(self.__mm_title_bg_texture, self.__mm_title_bg_rect)
        screen.blit(self.__button_play_texture, self.__play_button_rect)
        screen.blit(self.__button_info_texture, self.__info_button_rect)
        screen.blit(self.__button_quit_texture, self.__quit_button_rect)
        screen.draw_string("THE SNAKE", (250, 30))
        screen.draw_string("PLAY", (SCREEN_WIDTH / 2 - 30, SCREEN_HEIGHT / 2 - 115))
        screen.draw_string("INSTRUCTIONS", (SCREEN_WIDTH / 2 - 80, SCREEN_HEIGHT / 2 - 35))
        screen.draw_string("QUIT", (SCREEN_WIDTH / 2 - 30, SCREEN_HEIGHT / 2 + 50))
