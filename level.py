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
        # for i in range(50):
        #     maps[random.randrange(size)] = 2
        self._map = maps
        self.outterEdge()
        self.makeForest(10*LEVEL_WIDTH + 20,5)
        self.makeBuilding(10*LEVEL_WIDTH + 10, 2)

    def outterEdge(self):
        for i in range(LEVEL_WIDTH):
            self._map[i] = 3
            self._map[LEVEL_WIDTH * LEVEL_HEIGHT - 1 - i] = 3
            self._map[i*LEVEL_WIDTH] = 3
            self._map[i*(LEVEL_WIDTH)-1] = 3

    def makeBuilding(self, pos, size):
        for i in range(1+size):
            self._map[pos-size+i*LEVEL_WIDTH] = 3
            self._map[pos-size-i*LEVEL_WIDTH] = 3
            if i != 0:
                self._map[pos+size+i*LEVEL_WIDTH] = 3
                self._map[pos+size-i*LEVEL_WIDTH] = 3
            self._map[pos-size*LEVEL_WIDTH+i] = 3
            self._map[pos-size*LEVEL_WIDTH-i] = 3
            self._map[pos+size*LEVEL_WIDTH-i] = 3
            self._map[pos+size*LEVEL_WIDTH+i] = 3


    def makeForest(self, pos, size):
        for i in range(size):
            self._map[pos-i] = 2
            self._map[pos+i] = 2
            self._map[pos-LEVEL_WIDTH*i] = 2
            self._map[pos+LEVEL_WIDTH*i] = 2
            self._map[pos-LEVEL_WIDTH*i-i] = 2
            self._map[pos+LEVEL_WIDTH*i-i] = 2
            self._map[pos-LEVEL_WIDTH*i+i] = 2
            self._map[pos+LEVEL_WIDTH*i+i] = 2
    def makeZomArea(self, pos, power):
        pass

    def _pos (self,x,y):
        return x + (y*LEVEL_WIDTH);

    # return the tile at a given tile position in the level
    def tile (self,x,y):
        return self._map[self._pos(x,y)]
