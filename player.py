from character import *
from screen import *
#
# The Player character
#
class Player (Character):
    def __init__ (self,name):
        Character.__init__(self,name,"Yours truly")
        log("Player.__init__ for "+str(self))
        pic = 't_android_red.gif'
        self._sprite = Image(Point(TILE_SIZE/2,TILE_SIZE/2),pic)

    def is_player (self):
        return True


    # The move() method of the Player is called when you 
    # press movement keys. 
    # It is different enough from movement by the other
    # characters that you'll probably need to overwrite it.
    # In particular, when the Player move, the screen scrolls,
    # something that does not happen for other characters
   
    def move (self,dx,dy):
        nx = self._x + dx
        ny = self._y + dy
        if self._screen.tile(nx,ny) == 0 or self._screen.tile(nx,ny) == 1  or self._screen.tile(nx,ny)/10 >= 4:
            self._screen._level.set_tile(self._x,self._y,self._screen._level.tile(self._x,self._y)%10)
            self._y = ny
            self._x = nx
            self._screen._level.set_tile(self._x,self._y,3*10 + self._screen._level.tile(self._x,self._y))
            self._screen.move(dx, dy, nx, ny)
            for thing in self._screen._objects:
                thing.update_pos(dx, dy, nx, ny)




