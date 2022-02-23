from os.path import isfile, join

from constants import PATH
from pygame import mixer


class SoundManager():
    """ This class is responsible for reproduce sounds and music """
    
    def __init__(self) -> None:        
        mixer.pre_init()
        mixer.init()
        self.__load_resources()

    def __load_resources(self) -> None:
        """ Preloads sounds """
        self.__mouse_click_sound = mixer.Sound(join(PATH, 'res', 'sounds', 'click.wav'))
        self.__snake_eat_sound = mixer.Sound(join(PATH, 'res', 'sounds', 'snake_eat.mp3'))
        self.__level_up_sound = mixer.Sound(join(PATH, 'res', 'sounds', 'oh_yeah.wav'))
        try:
            music_file = join(PATH, 'res', 'music', 'music.mp3')
            if isfile(music_file):
                mixer.music.load(music_file)
                mixer.music.play(loops=-1)
                mixer.music.set_volume(.5)
        except:
            print("Unable to load music file")
    
    def play_click_sound(self) -> None:
        """ Plays mouse click sound """
        mixer.Channel(0).play(self.__mouse_click_sound)
        return

    def play_eating_sound(self) -> None:
        """ Plays the sound when the snake eats an object """
        mixer.Channel(1).play(self.__snake_eat_sound, maxtime=2000) # Just reproduce first 2 seconds.
        return

    def play_level_up_sound(self) -> None:
        """ Plays level up sound """
        mixer.Channel(2).play(self.__level_up_sound)
        return
