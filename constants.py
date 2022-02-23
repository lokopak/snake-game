from os.path import dirname, realpath

# Absolute path to avoid file reading errors.
PATH = dirname(realpath(__file__))

'''
 Global constants
'''

# Screen refresh rate (60 frames per second)
FPS = 60

# Colors
WHITE  = (222, 238, 214)
BLACK  = (  0,   0,   0)
GREEN  = (  0, 155,   0)
RED    = (255,   0,   0)
BLUE   = (  0,   0, 255)
YELLOW = (255, 255,   0)

# Screen dimensions
SCREEN_WIDTH  = 600
SCREEN_HEIGHT = 600

# Game cell dimensions
CELL_SIZE   = 20

# Directions
UP    = 0
RIGHT = 1
DOWN  = 2
LEFT  = 3

# Game states
MENU          = 0
INSTRUCTIONS  = 1
PLAY          = 2
PAUSED        = 3
GAME_OVER     = 4

# Levels
LEVEL = 1

# Game grid (game play area limits)
MIN_X = 10 # Min horizontal screen coordinate
MIN_Y = 130 # Min vertical screen coordinate
MAX_X = SCREEN_WIDTH - 10 # Max horizontal screen coordinate
MAX_Y = SCREEN_HEIGHT - 10 # Max vertical screen coordinate
GRID_CELLS = (MAX_X - MIN_X) // CELL_SIZE # 600 - 60 * 2 / 40 cells
