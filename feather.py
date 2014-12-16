from thing import *


class Feather  (Thing):
    def __init__ (self,name,desc, health):
        Thing.__init__(self,name,desc, health)
        log("Character.__init__ for "+str(self))
        rect = Rectangle(Point(1,1),
                         Point(TILE_SIZE-1,TILE_SIZE-1))
        rect.setFill("yellow")
        rect.setOutline("yellow")
        self._sprite = rect
        self._user = None
        self._price = 10

    def use(self):
        self._health = self._health - 1
        if self._health <= 0:
            self.die()

    def pickup(self, user):
        self._user = user

    def die(self):
        if self._user != None:
            self._user._inventory.remove(self)
        else:
            OBJECTS.remove(self)
            self._sprite.undraw()
            print self._name + "has died"

    def is_character (self):
        return False

    def is_walkable (self):
        return True
