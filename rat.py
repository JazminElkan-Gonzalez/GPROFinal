from character import *
import time

# 
# A Rat is an example of a character which defines an event that makes
# the rat move, so that it can be queued into the event queue to enable
# that behavior. (Which is right now unfortunately not implemented.)
#
class Rat (Character):
    def __init__ (self,name,desc, health):
        Character.__init__(self,name,desc, health)
        log("Rat.__init__ for "+str(self))
        rect = Rectangle(Point(1,1),
                         Point(TILE_SIZE-1,TILE_SIZE-1))
        rect.setFill("red")
        rect.setOutline("red")
        self._sprite = rect
        print "Type rat: ", type(rect)
        self._direction = random.randrange(4)

    # A helper method to register the Rat with the event queue
    # Call this method with a queue and a time delay before
    # the event is called
    # Note that the method returns the object itself, so we can
    # use method chaining, which is cool (though not as cool as
    # bowties...)

    # this gets called from event queue when the time is right

    def event (self,q):
        self.attack()
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
        
    def attack(self):
        for thing in OBJECTS:
            if (thing._x == self._x and thing._y == self._y -1) or (thing._x == self._x and thing._y == self._y + 1) or  (thing._x == self._x + 1 and thing._y == self._y) or  (thing._x == self._x - 1 and thing._y == self._y):
                thing.updateHealth(-5)