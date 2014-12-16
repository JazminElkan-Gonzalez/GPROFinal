from thing import *


class Feather  (Thing):
    def __init__ (self,name,desc, health):
        Thing.__init__(self,name,desc, health)
        log("Character.__init__ for "+str(self))
        rect = Rectangle(Point(1,1),
                         Point(TILE_SIZE-1,TILE_SIZE-1))
        rect.setFill("red")
        rect.setOutline("red")
        self._sprite = rect

    def use(self, user):
        self._health = self._health - 1
        if self._health <= 0:
            self.die(user) 


    def die(self, user):
        user._inventory.remove(self)

            
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
