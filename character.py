from thing import *
import math

# Characters represent persons and animals and things that move
# about possibly proactively
#
class Character (Thing):
    def __init__ (self,name,desc, health, items):
        Thing.__init__(self,name,desc, health)
        log("Character.__init__ for "+str(self))
        rect = Rectangle(Point(1,1),
                         Point(TILE_SIZE-1,TILE_SIZE-1))
        rect.setFill("red")
        rect.setOutline("red")
        self._sprite = rect
        self._items = items
        for i in range(len(self._items)):
            xDef = 80 + (i%10)*(TILE_SIZE+2) 
            yDef = WINDOW_HEIGHT + 100 + math.floor(i/10)*(TILE_SIZE+2)
            items[i].pickup(self)
            items[i]._sprite.move(xDef - items[i]._sprite.p1.x, yDef - items[i]._sprite.p1.y)

    # A character has a move() method that you should implement
    # to enable movement


    def addInventory(self, item):
        self._items.append(item)

    def move (self,dx,dy):
        nx = self._x + dx
        ny = self._y + dy
        if self._screen.tile(nx,ny) == 0:
            if self._screen.tile(nx,ny):
                self._sprite.move(dx*TILE_SIZE,dy*TILE_SIZE)
   

    def is_character (self):
        return True

    def is_walkable (self):
        return False
