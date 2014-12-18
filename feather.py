from thing import *


class Feather  (Thing):
    def __init__ (self,name,desc, health):
        Thing.__init__(self,name,desc, health)
        rect = Rectangle(Point(1,1),
                         Point(TILE_SIZE-1,TILE_SIZE-1))
        rect.setFill("yellow")
        rect.setOutline("yellow")

        self._pic = 'feather.gif'
        self._sprite = Image(Point(TILE_SIZE/2,TILE_SIZE/2),self._pic)

        # self._sprite = rect
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

    def is_character (self):
        return False

    def is_walkable (self):
        return True
