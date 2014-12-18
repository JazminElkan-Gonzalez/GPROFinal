#############################################################
# 
# The description of the world and the screen which displays
# the world
#
# A level contains the background stuff that you can't really
# interact with. The tiles are decorative, and do not come
# with a corresponding object in the world.
#
# Right now, a level is described using the following encoding
#
# 0 empty
# 1 grass
# 2 tree
# 3 wall    
# the level has set buildings and then random zombies thrown about
from util import *
from tree import *


class Level (object):
    def __init__ (self):
        size = LEVEL_WIDTH * LEVEL_HEIGHT
        maps = [0] * size
        for i in range(100):
            maps[random.randrange(size)] = 1
        for i in range(50):
            maps[random.randrange(size)] = 2
        self._map = maps
        self.outterEdge()
        self.makeBuilding(7*LEVEL_WIDTH  + LEVEL_WIDTH-20, 2,2, "S")
        self.makeBuilding(10*LEVEL_WIDTH + LEVEL_WIDTH-10,6,6,"W")
        self.makeBuilding(13*LEVEL_WIDTH  + LEVEL_WIDTH-23, 4,2, "N")
        self.makeBuilding(7*LEVEL_WIDTH  + LEVEL_WIDTH-26, 2,2, "S")

# Creats an outter edge around the world so that the player and zombies cannot
# walk off the map
    def outterEdge(self):
        for i in range(LEVEL_WIDTH):
            self._map[i] = 3
            self._map[LEVEL_WIDTH * LEVEL_HEIGHT - 1 - i] = 3
            self._map[i*LEVEL_WIDTH] = 3
            self._map[i*(LEVEL_WIDTH)-1] = 3

# Makes a building of a given size at a given location
# Uses the direction indicated by "door" to create a window
# Bildings are simply 4 walls 
    def makeBuilding(self, pos, length, width, door):
        for i in range(1+width):
            self._map[pos-length+i*LEVEL_WIDTH] = 3
            self._map[pos-length-i*LEVEL_WIDTH] = 3
            self._map[pos+length+i*LEVEL_WIDTH] = 3
            self._map[pos+length-i*LEVEL_WIDTH] = 3
        for i in range(1+length):
            self._map[pos-width*LEVEL_WIDTH+i] = 3
            self._map[pos-width*LEVEL_WIDTH-i] = 3
            self._map[pos+width*LEVEL_WIDTH-i] = 3
            self._map[pos+width*LEVEL_WIDTH+i] = 3
            if door == "W":
                self._map[pos-length] = 0 
            if door == "E":
                self._map[pos+length] = 0 
            if door == "N":
                self._map[pos-width*LEVEL_WIDTH] = 0 
            if door == "S":
                self._map[pos+width*LEVEL_WIDTH] = 0 

# A helper function for makeDecay. It checks to make sure that the function does not try to access space outside of the map
    def areaRange(self, value):
        if value < len(self._map)-1 and value > 0 and self._map[value] != 3:
            self._map[value] = 1

# Creates an area of "decay" around the zombie gravestones. This decay helps indicate the power level of the zombie
    def makeDecay(self, pos, size):
        for i in range(int(size)):
            self.areaRange(pos-i)
            self.areaRange(pos+i)
            self.areaRange(pos-LEVEL_WIDTH*i)
            self.areaRange(pos+LEVEL_WIDTH*i)
            for w in range(i+1):
                self.areaRange(pos-LEVEL_WIDTH*i-w)
                self.areaRange(pos+LEVEL_WIDTH*i-w)
                self.areaRange(pos-LEVEL_WIDTH*i+w)
                self.areaRange(pos+LEVEL_WIDTH*i+w)
                self.areaRange(pos-i-w*LEVEL_WIDTH)
                self.areaRange(pos+i-w*LEVEL_WIDTH)
                self.areaRange(pos-i+w*LEVEL_WIDTH)
                self.areaRange(pos+i+w*LEVEL_WIDTH)


# converts the x,y coordinate to a position in terms of the map
    def _pos (self,x,y):
        return x + (y*LEVEL_WIDTH);

# return the tile at a given tile position in the level
    def tile (self,x,y):
        return self._map[self._pos(x,y)]
