from character import *

# 
# A Rat is an example of a character which defines an event that makes
# the rat move, so that it can be queued into the event queue to enable
# that behavior. (Which is right now unfortunately not implemented.)
#
class Zombie (Character):
    def __init__ (self,name,desc,health):
        Character.__init__(self,name,desc, health)
        log("Zombie.__init__ for "+str(self))
        rect = Rectangle(Point(1,1),
                         Point(TILE_SIZE-1,TILE_SIZE-1))
        rect.setFill("darkgreen")
        rect.setOutline("red")
        self._sprite = rect

        self._status = "gravestone"

    # A helper method to register the Rat with the event queue
    # Call this method with a queue and a time delay before
    # the event is called
    # Note that the method returns the object itself, so we can
    # use method chaining, which is cool (though not as cool as
    # bowties...)

    # this gets called from event queue when the time is right

    def walk(self,dx,dy):
        pass

    def wakeUp(self):
        if self._status == "gravestone":
            self._status = "enemy"
        else:
            words = Text(self._sprite.p1, "GRR")
            words.draw(self._screen._window)
            self._screen.addText(words)

    def event (self,q):
        words = self.attack()
        direc = random.randint(0,3)
        if direc == 0:
            self.walk(1,0)
        if direc == 1:
            self.walk(-1,0)
        if direc == 2:
            self.walk(0,-1)
        if direc == 3:
            self.walk(0,1)
        #words.undraw()
        self.attack()
        log("event for "+str(self))
        self.register(q,self._freq)
        
    def attack(self):
        if self._status == "gravestone":
            pass
        elif self._status == "enemy":
            for thing in OBJECTS:
                if (thing._x == self._x and thing._y == self._y -1) or (thing._x == self._x and thing._y == self._y + 1) or  (thing._x == self._x + 1 and thing._y == self._y) or  (thing._x == self._x - 1 and thing._y == self._y):
                    thing._health = thing._health - 5
                    words = Text(self._sprite.p1, "SQUEE")
                    words.draw(self._screen._window)
                    return words