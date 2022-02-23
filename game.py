import random
from os import path

import pygame
from pygame import QUIT as QUIT_EVENT
from pygame import event
from pygame.time import Clock

from constants import *
from graphics.screen import Screen
from sound.sound_manager import SoundManager
from state.game_over_state import GameOverState
from state.game_state import GameState
from state.info_state import InfoState
from state.main_manu_state import MainMenuState
from state.play_state import PlayState
from state.quit_menu_state import QuitMenuState


class Game:
    
    __state: GameState
    
    def __init__(self) -> None:
        '''
        Game initialization
        '''
        pygame.init()
        self.__sound = SoundManager()
        self.__screen = Screen(self)
        self.__clock = Clock()

        # Flag to control that the game is running
        self.__running = False
        # Game state
        self.__status = MENU
        
    def get_screen(self) -> Screen:
        """ Returns game screen """
        return self.__screen
    
    def get_state(self) -> GameState:
        """ Returns current game state """
        return self.__state
    
    def get_sound_manager(self) -> SoundManager:
        """ Returns game sound manager """
        return self.__sound
    
    def get_status(self) -> int:
        """ Returns game status """
        return self.__status
    
    def set_status(self, status: int) -> None:
        """ Sets game status """
        
        self.__status = status
        
        # Otherwise, change state
        if self.__status == MENU:
            self.__state = MainMenuState(self)
        elif self.__status == INSTRUCTIONS:
            self.__state = InfoState(self)
        elif self.__status == PLAY:
            self.__state = PlayState(self)
        elif self.__status == GAME_OVER:
            self.__state = GameOverState(self)

    def __process_input(self) -> None:
        """ Here should go the handling of input events (mouse, keyboard...) """
        input = event.get()
        
        for e in input:
            if e.type == QUIT_EVENT:
                self.quit()
                return
        
        if self.__state:
            self.__state.process_input(input)

    def __game_update(self):
        """ This is where the logic of the game should go """
        if self.__state:
            self.__state.update(0)

    def __render_screen(self):
        """ Here should go the update of the screen images """
        if self.__state:
            self.__state.render(self.__screen)
        
        self.__screen.update_cursor()
        pygame.display.flip()

    def quit(self, force: bool = False) -> None:
        """ Exits from game """
        if force or self.__status == QUIT_STATUS:
            self.__running = False
        else:
            self.__status = QUIT_STATUS
            self.__state = QuitMenuState(self)
            
    def cancel_quit(self) -> None:
        # If we were running in QUIT state and change state, just back to previous state
        if self.__status == QUIT_STATUS and isinstance(self.__state, QuitMenuState):
            self.__state = self.__state.get_parent()
            self.__status = self.__state.get_status()
            return
        
    def run_game(self):
        """ Game main loop """
        self.__state = MainMenuState(self)

        self.__running = True
        while self.__running:
            self.__process_input()
            self.__game_update()
            self.__render_screen()
            self.__clock.tick(FPS)
