from character import *
from screen import *
#
# The Player character
#
class Player (Character):
    def __init__ (self,health,name):
        Character.__init__(self,name,"Yours truly", health)
        log("Player.__init__ for "+str(self))
        pic = 't_android_red.gif'
        self._sprite = Image(Point(TILE_SIZE/2,TILE_SIZE/2),pic)

    def is_player (self):
        return True

    def update_pos(self, dx, dy):
        pass


    # The move() method of the Player is called when you 
    # press movement keys. 
    # It is different enough from movement by the other
    # characters that you'll probably need to overwrite it.
    # In particular, when the Player move, the screen scrolls,
    # something that does not happen for other characters
   
    def move (self,dx,dy):
        nx = self._x + dx
        ny = self._y + dy
        if self._screen.tile(nx,ny) == 0 or self._screen.tile(nx,ny) == 1:
            for i in range(len(OBJECTS)):
                if OBJECTS[i]._x == nx and  OBJECTS[i]._y == ny:
                    if OBJECTS[i].is_walkable():
                        self._y = ny
                        self._x = nx
                        self._screen.move(dx, dy)
                        for thing in OBJECTS:
                            # if thing._name !=  "...what's your name, bub?...":
                            thing.update_pos(dx, dy)
                    break
                elif i == len(OBJECTS) -1:
                    self._y = ny
                    self._x = nx
                    self._screen.move(dx, dy)
                    for thing in OBJECTS:
                        # if thing._name !=  "...what's your name, bub?...":
                        thing.update_pos(dx, dy)




