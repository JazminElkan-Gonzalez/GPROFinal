from thing import *
#
# Characters represent persons and animals and things that move
# about possibly proactively
#
class Character (Thing):
    def __init__ (self,name,desc):
        Thing.__init__(self,name,desc)
        log("Character.__init__ for "+str(self))
        rect = Rectangle(Point(1,1),
                         Point(TILE_SIZE-1,TILE_SIZE-1))
        rect.setFill("red")
        rect.setOutline("red")
        self._sprite = rect

    # A character has a move() method that you should implement
    # to enable movement

    def move (self,dx,dy):
        nx = self._x + dx
        ny = self._y + dy
        self._sprite.move(dx*TILE_SIZE,dy*TILE_SIZE)
   

    def is_character (self):
        return True

    def is_walkable (self):
        return False
