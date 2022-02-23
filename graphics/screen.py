from os.path import join
from typing import Tuple

from constants import PATH, SCREEN_HEIGHT, SCREEN_WIDTH
from pygame import Rect, Surface, display, image, mouse


class Screen:
    """ This class is responsible for drawing elements on the screen """
    
    __cursor: Surface = None
    
    def __init__(self, game) -> None:
        self.__canvas = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        display.set_caption('The Snake')
        mouse.set_visible(False)
        self.__load_resources()
        
    def __load_resources(self) -> None:
        """ Pre-loads required resources like cursor texture """ 
        self.__cursor = image.load(join(PATH, 'res', 'images', 'mouse_icon.png'))
        
    def fill(self, color, rect: Tuple = None) -> Rect:
        """ Fills screen surface with a given solid color """
        return self.__canvas.fill(color, rect)
    
    def blit(self, surface: Surface, dest: Tuple) -> Rect:
        """ Draws an image onto screen surface """
        return self.__canvas.blit(surface, dest)

    def update_cursor(self):
        """ Updates mouse cursor position """
        self.blit(self.__cursor, mouse.get_pos())
        return
