
from os.path import join

from constants import (BLACK, PATH, QUIT_STATUS, SCREEN_HEIGHT, SCREEN_WIDTH,
                       WHITE)
from graphics.font import FontType
from graphics.screen import Screen
from pygame import MOUSEBUTTONDOWN, Rect
from pygame.image import load

from state.game_state import GameState


class QuitMenuState(GameState):
    """ Quit menu state screen """
    
    """ Parent game state to back to when quit process is canceled """
    __parent: GameState
    
    _status = QUIT_STATUS
    
    def __init__(self, game) -> None:
        super().__init__(game)
        # Sets previous state to back to in case quit process is canceled
        self.__parent = self._game.get_state()
        self._load_resources()
        
    def get_parent(self) -> GameState:
        """ Returns parent game state """
        return self.__parent
        
    def _load_resources(self) -> None:
        """ Loads necessary resources for this state """        
        self.__qc_menu_if_texture  = load(join(PATH, 'res', 'images', 'quit_menu_interface.png'))
        self.__interface_rect = self.__qc_menu_if_texture.get_rect()
        self.__interface_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        
        # We get buttons rectangles
        self.__cancel_button_rect  = Rect(SCREEN_WIDTH / 2 + 148, SCREEN_HEIGHT / 2 - 32, 32, 32)
        self.__confirm_button_rect = Rect(SCREEN_WIDTH / 2 + 148, SCREEN_HEIGHT / 2, 32, 32)

        self.__confirm_text = "Are you sure?"
        
    def get_status(self) -> int:
        return self._status
        
    def process_input(self, input) -> None:
        """ Process inputs """
        for event in input:
            if event.type == MOUSEBUTTONDOWN:
                if self.__confirm_button_rect.collidepoint(event.pos):
                    self._game.get_sound_manager().play_click_sound()
                    self._game.quit(True)
                # We simply exit the loop to finish and return to the previous screen
                elif self.__cancel_button_rect.collidepoint(event.pos):
                    self._game.get_sound_manager().play_click_sound()
                    self._game.cancel_quit()
                
    def update(self, time: int) -> None:
        """ Updates the state """
        pass
    
    def render(self, screen: Screen) -> None:
        """ Renders the confirmation menu to quit the game """    
        screen.fill(BLACK)
        
        screen.blit(self.__qc_menu_if_texture, self.__interface_rect)
        screen.draw_string(self.__confirm_text, (SCREEN_WIDTH / 2 - 90, SCREEN_HEIGHT / 2 - 15), FontType.MD, color=WHITE)
