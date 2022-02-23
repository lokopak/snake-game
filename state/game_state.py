from abc import ABC, abstractmethod, abstractproperty
from typing import List

from graphics.screen import Screen
from pygame.event import Event


class GameState(ABC):
    """ Game state abstract class """
    

    def __init__(self, game) -> None:
        super().__init__()
        self._game = game
        
    @abstractproperty
    def get_status(self) -> int:
        """
        Return the game status associated with this state.
        Every game status should define its own status.
        """
        pass
    
    def get_game(self):
        return self._game
    
    @abstractmethod
    def update(self, time: int) -> None:
        """ Updates the state """
        pass

    @abstractmethod    
    def process_input(self, input: List[Event]) -> None:
        """ Process inputs """
        pass
    
    @abstractmethod
    def render(self, screen: Screen) -> None:
        """ Renders the confirmation menu to quit the game """
        pass
