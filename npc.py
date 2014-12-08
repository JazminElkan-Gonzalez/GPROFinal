from character import *
import time

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

    def event (self,q):
        log("event for "+str(self))
        self.register(q,self._freq)
        
    def talk(self):
        words = Text(self._sprite.anchor, knowledge)
        words.draw(self._screen._window)
        self._screen.addText(words)

    def sell(self):
        pass

    def heal(self,character):
        pass