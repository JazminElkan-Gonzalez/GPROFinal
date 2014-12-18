#############################################################
#
# A Statue that is placed at the enterence of the game
# Tells the player the initial story
#

from thing import *

class OlinStatue (Thing):
    def __init__ (self,name,desc, health):
        Thing.__init__(self,name,desc, health)
        self._pic = 'statue.gif'
        self._sprite = Image(Point(TILE_SIZE/2,TILE_SIZE/2),self._pic)
