from character import *
import time
from screen import *

class NPC (Character):
    def __init__ (self,name,desc, health, knowledge, items, prices):
        Character.__init__(self,name,desc, health)
        log("NPC.__init__ for "+str(self))
        rect = Rectangle(Point(1,1),
                         Point(TILE_SIZE-1,TILE_SIZE-1))
        rect.setFill("blue")
        rect.setOutline("blue")
        self._sprite = rect
        self._direction = random.randrange(4)
        self._knowledge = knowledge
        self._items = items
        self._prices = prices

    def event (self,q):
        log("event for "+str(self))
        self.register(q,self._freq)
        
    def talk(self):
        self._screen.makeDialogue("talk", self._name, self._knowledge, self._items, self._prices)

    def sell(self):
        self._screen.makeDialogue("sell", self._name, self._knowledge, self._items, self._prices)


    def heal(self):
        self._screen.makeDialogue("heal", self._name, self._knowledge, self._items, self._prices)

