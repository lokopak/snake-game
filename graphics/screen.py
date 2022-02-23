from typing import Any, Tuple

from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from pygame import Rect, Surface, display, mouse


class Screen:
    """ This class is responsible for drawing elements on the screen """
    
    def __init__(self, game) -> None:
        self.__canvas = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        display.set_caption('The Snake')
        mouse.set_visible(False)
        
    def fill(self, color, rect: Tuple = None) -> Rect:
        """ Fills screen surface with a given solid color"""
        return self.__canvas.fill(color, rect)
    
    def blit(self, surface: Surface, dest: Rect) -> Rect:
        """" Draws an image onto screen surface """
        return self.__canvas.blit(surface, dest)
