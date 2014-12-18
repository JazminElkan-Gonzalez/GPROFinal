from thing import *
import math

class Character (Thing):
    def __init__ (self,name,desc, health, items):
        Thing.__init__(self,name,desc, health)
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
            if isinstance(items[i]._sprite, Rectangle):
                items[i]._sprite.move(xDef - items[i]._sprite.p1.x, yDef - items[i]._sprite.p1.y)
            elif isinstance(items[i]._sprite, Image):
                items[i]._sprite.move(xDef - items[i]._sprite.getAnchor().x+TILE_SIZE/2, yDef - items[i]._sprite.getAnchor().y+TILE_SIZE/2)

    def addInventory(self, item):
        self._items.append(item)

    def move (self,dx,dy):
        nx = self._x + dx
        ny = self._y + dy
        if self._screen.tile(nx,ny) == 0:
            if self._screen.tile(nx,ny):
                self.moveSprite(dx*TILE_SIZE,dy*TILE_SIZE)
   

    def is_character (self):
        return True

    def is_walkable (self):
        return False
