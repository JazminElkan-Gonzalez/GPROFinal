from thing import *
#
# Characters represent persons and animals and things that move
# about possibly proactively
#
class Tree (Thing):
    def __init__ (self,name,desc, y, x):
        Thing.__init__(self,name,desc)
        log("Character.__init__ for "+str(self))
        rect = Rectangle(Point(1,1),
                         Point(TILE_SIZE-1,TILE_SIZE-1))
        rect.setFill("red")
        rect.setOutline("red")
        self._sprite = rect
        self._x = x
        self._y = y

   
    def is_walkable (self):
        return False
