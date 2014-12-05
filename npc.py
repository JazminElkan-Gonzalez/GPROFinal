from character import *
import time

# 
# A Rat is an example of a character which defines an event that makes
# the rat move, so that it can be queued into the event queue to enable
# that behavior. (Which is right now unfortunately not implemented.)
#
class NPC (Character):
    def __init__ (self,name,desc, health, knowledge, items, prices):
        Character.__init__(self,name,desc, health)
        log("NPC.__init__ for "+str(self))
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

    # this gets called from event queue when the time is right

    def event (self,q):
        log("event for "+str(self))
        self.register(q,self._freq)
        
    def talk(self):
        if isinstance(self._sprite, Image):
            words = Text(self._sprite.anchor, knowledge)
        else:
            words = Text(self._sprite.p1, knowledge)

    def sell(self):
        pass

    def heal(self,character):
        pass