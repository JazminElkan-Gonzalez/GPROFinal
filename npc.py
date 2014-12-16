from character import *
import time
from screen import *

class NPC (Character):
    def __init__ (self,name,desc, health, knowledge, items):
        Character.__init__(self,name,desc, health, items)
        log("NPC.__init__ for "+str(self))
        rect = Rectangle(Point(1,1),
                         Point(TILE_SIZE-1,TILE_SIZE-1))
        rect.setFill("blue")
        rect.setOutline("blue")
        self._sprite = rect
        self._direction = random.randrange(4)
        self._knowledge = knowledge

    def sold(self,item, player):
        self._items.remove(item)
        player.changeGold(-item._price)
        player.addInventory(item)
        self._screen._dButtons.remove(item)


    def event (self,q):
        log("event for "+str(self))
        self.register(q,self._freq)
        
    def talk(self):
        self._screen.makeDialogue("talk", self._name, self._knowledge, self._items)

    def sell(self):
        self._screen.makeDialogue("sell", self._name, self._knowledge, self._items)


    def heal(self):
        self._screen.makeDialogue("heal", self._name, self._knowledge, self._items)

