#############################################################
# 
# The description of the world and the screen which displays
from util import *
from tree import *
# the world
#
# A level contains the background stuff that you can't really
# interact with. The tiles are decorative, and do not come
# with a corresponding object in the world. (Though you can
# change that if you want.)
#
# Right now, a level is described using the following encoding
#
# 0 empty   (light green rectangle)
# 1 grass   (green rectangle)
# 2 tree    (sienna rectangle)
# 30s unwalkable     (color depends)
# 40s walkable       (color depends)
# you'll probably want to make nicer sprites at some point.


#
# This implements a random level right now. 
# You'll probably want to replace this with something that 
# implements a specific map -- perhaps of Olin?
#



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
        #self.makeForest(10*LEVEL_WIDTH + LEVEL_WIDTH - 20,5)
        #self.makeForest(21*LEVEL_WIDTH + LEVEL_WIDTH - 20,5)
        self.makeBuilding(7*LEVEL_WIDTH  + LEVEL_WIDTH-20, 2,2, "S")
        self.makeBuilding(10*LEVEL_WIDTH + LEVEL_WIDTH-10,6,6,"W")
        #self.makeBuilding(13*LEVEL_WIDTH  + LEVEL_WIDTH-20, 2,2, "N")
        self.makeBuilding(13*LEVEL_WIDTH  + LEVEL_WIDTH-23, 4,2, "N")
        self.makeBuilding(7*LEVEL_WIDTH  + LEVEL_WIDTH-26, 2,2, "S")


    def outterEdge(self):
        for i in range(LEVEL_WIDTH):
            self._map[i] = 3
            self._map[LEVEL_WIDTH * LEVEL_HEIGHT - 1 - i] = 3
            self._map[i*LEVEL_WIDTH] = 3
            self._map[i*(LEVEL_WIDTH)-1] = 3

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

    def makeForest(self, pos, size):
        for i in range(size):
            self._map[pos-i] = 2
            self._map[pos+i] = 2
            self._map[pos-LEVEL_WIDTH*i] = 2
            self._map[pos+LEVEL_WIDTH*i] = 2
            for w in range(i+1):
                self._map[pos-LEVEL_WIDTH*i-w] = 2
                self._map[pos+LEVEL_WIDTH*i-w] = 2
                self._map[pos-LEVEL_WIDTH*i+w] = 2
                self._map[pos+LEVEL_WIDTH*i+w] = 2
                self._map[pos-i-w*LEVEL_WIDTH] = 2
                self._map[pos+i-w*LEVEL_WIDTH] = 2
                self._map[pos-i+w*LEVEL_WIDTH] = 2
                self._map[pos+i+w*LEVEL_WIDTH] = 2
    def makeZomArea(self, pos, power):
        pass

    def _pos (self,x,y):
        return x + (y*LEVEL_WIDTH);

    # return the tile at a given tile position in the level
    def tile (self,x,y):
        return self._map[self._pos(x,y)]
