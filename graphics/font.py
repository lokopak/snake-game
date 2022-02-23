from enum import IntEnum
from typing import Tuple

from constants import WHITE
from pygame import Surface
from pygame.font import SysFont


class FontType(IntEnum):
    """ Available font types """
    SM = 0,
    MD = 1,
    LG = 2

class Font:
    """ This class is responsible for manage fonts and generate text images """
    __font_sm: SysFont
    __font_md: SysFont
    __font_lg = SysFont
    
    def __init__(self) -> None:
        self.__load_resources()
        
    def __load_resources(self) -> None:    
        """ Preload fonts that we are going to use """
        self.__font_sm = SysFont('Comic Sans MS', 16)
        self.__font_md = SysFont('Comic Sans MS', 20, True)
        self.__font_lg = SysFont('Comic Sans MS', 40, True, True)
        
    def draw_string(self, string: str, font: FontType = FontType.SM, color: Tuple[int, int, int] = WHITE) -> Surface:
        """ Generate a surface with rendered text """
        if font == FontType.SM:
            _font = self.__font_sm
        elif font == FontType.LG:
            _font = self.__font_lg
        else:
            _font = self.__font_md
            
        return _font.render(string, True, color)
