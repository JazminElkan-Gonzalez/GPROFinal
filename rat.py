from character import *


# 
# A Rat is an example of a character which defines an event that makes
# the rat move, so that it can be queued into the event queue to enable
# that behavior. (Which is right now unfortunately not implemented.)
#
class Rat (Character):
    def __init__ (self,name,desc):
        Character.__init__(self,name,desc)
        log("Rat.__init__ for "+str(self))
        rect = Rectangle(Point(1,1),
                         Point(TILE_SIZE-1,TILE_SIZE-1))
        rect.setFill("red")
        rect.setOutline("red")
        self._sprite = rect
        self._direction = random.randrange(4)

    # A helper method to register the Rat with the event queue
    # Call this method with a queue and a time delay before
    # the event is called
    # Note that the method returns the object itself, so we can
    # use method chaining, which is cool (though not as cool as
    # bowties...)

    def register (self,q,freq):
        self._freq = freq
        q.enqueue(freq,self)
        return self

    def walk(self, dx, dy):
        nx = self._x + dx
        ny = self._y + dy
        if self._screen.tile(nx,ny) == 0 or self._screen.tile(nx,ny) == 1  or self._screen.tile(nx,ny)/10 >= 4:
            self._screen._level.set_tile(self._x,self._y,self._screen._level.tile(self._x,self._y)%10)
            self._y = ny
            self._x = nx
            self._sprite.move(-dx*TILE_SIZE,-dy*TILE_SIZE)
            if self._sprite.p1.x < 0 and self._sprite.p1.x/TILE_SIZE +1 > VIEWPORT_WIDTH and self._sprite.p1.y < 0 and self._sprite.p1.y/TILE_SIZE + 1 > VIEWPORT_HEIGHT:
                self._sprite.undraw()
            self._screen._level.set_tile(self._x,self._y,3*10 + self._screen._level.tile(self._x,self._y))


    def materialize (self,screen,x,y):
        screen.add(self,x,y)
        self._screen = screen
        self._screen._objects.append(self)
        self._x = x
        self._y = y
        return self

    # this gets called from event queue when the time is right

    def event (self,q):
        direc = random.randint(0,3)
        if direc == 0:
            self.walk(1,0)
        if direc == 1:
            self.walk(-1,0)
        if direc == 2:
            self.walk(0,-1)
        if direc == 3:
            self.walk(0,1)
        log("event for "+str(self))
        self.register(q,self._freq)
        