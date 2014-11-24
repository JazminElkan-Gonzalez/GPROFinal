from thing import *
#
# Example of a kind of thing with its specific sprite
# (here, a rather boring gray rectangle.)
#
class OlinStatue (Thing):
    def __init__ (self):
        Thing.__init__(self,"Olin statue","A statue of F. W. Olin")
        rect = Rectangle(Point(1,1),Point(TILE_SIZE-1,TILE_SIZE-1))
        rect.setFill("gray")
        rect.setOutline("gray")
        self._sprite = rect
