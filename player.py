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
        self._healthBar = Rectangle(Point(WINDOW_WIDTH+TILE_SIZE,TILE_SIZE),Point(WINDOW_WIDTH+WINDOW_RIGHTPANEL-TILE_SIZE,2*TILE_SIZE))



    def is_player (self):
        return True

    def update_pos(self, dx, dy):
        pass

    def updateHealth(self, amount):
        self._health = self._health + amount
        if self._health > 0:
            if isinstance(self._sprite, Image):
                words = Text(self._sprite.anchor, "SQUEE")
            else:
                words = Text(self._sprite.p1, "SQUEE")
            words.draw(self._screen._window)
            self._screen.addText(words)
            self._healthBar.undraw()
            addLength = (WINDOW_RIGHTPANEL - 2*TILE_SIZE)*self._health/self._maxHealth
            self._healthBar = Rectangle(Point(WINDOW_WIDTH+TILE_SIZE,TILE_SIZE),Point(WINDOW_WIDTH+TILE_SIZE + addLength,2*TILE_SIZE))
            self._healthBar.setFill("red")
            self._healthBar.draw(self._screen._window)
            self._preHealth.undraw()
            self._preHealth = Text(Point(WINDOW_WIDTH+1.5*TILE_SIZE,1.5*TILE_SIZE), str(self._health))
            self._preHealth.draw(self._screen._window)

        else:
            self._healthBar.undraw()
            lost(self._screen._window)

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
                            thing.update_pos(dx, dy)
                    break
                elif i == len(OBJECTS) -1:
                    self._y = ny
                    self._x = nx
                    self._screen.move(dx, dy)
                    for thing in OBJECTS:
                        thing.update_pos(dx, dy)





    def materialize (self,screen,x,y):
        screen.add(self,x,y)
        self._screen = screen
        self._x = x
        self._y = y
        outside = Rectangle(Point(WINDOW_WIDTH+TILE_SIZE,TILE_SIZE),Point(WINDOW_WIDTH+WINDOW_RIGHTPANEL-TILE_SIZE,2*TILE_SIZE))
        outside.setFill("lightgray")
        outside.setOutline("black")
        outside.draw(self._screen._window)
        self._healthBar.setFill("red")
        self._healthBar.draw(self._screen._window)
        self._preHealth = Text(Point(WINDOW_WIDTH+1.5*TILE_SIZE,1.5*TILE_SIZE), str(self._health))
        self._preHealth.draw(self._screen._window)
        self._maxHealth = self._health
        return self
