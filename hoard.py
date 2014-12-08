from util import *
from character import *
from npc import *
from player import *

class Hoard (Character):
    def __init__ (self,name,desc,zombies):
        Zombie.__init__(self,name,desc,0)
        log("Hoard.__init__ for "+str(self))
        rect = Rectangle(Point(1,1),
                         Point(TILE_SIZE-1,TILE_SIZE-1))
        rect.setFill("red")
        rect.setOutline("green")
        self._sprite = rect

        self._health = 0
        self._power = 0
        self._zombies = []
        for zombie in zombies:
            self._power = self._power + zombie._power
            self._health = self._health + zombie._health
            self.addZombie(zombie)

        self._status = "friend"
        self._movement = "follow"

    def zombieNum(self):
        return len(self._zombies)

    def addZombie(self,zombie):
        self._zombies.append(zombie)
        self._health = self._health + zombie._health
        self._power = self._power + zombie._power

        zombie._hoard = self

    def combine(self,partner):
        if isinstance(partner, Zombie):
            self.addZombie(partner)
        elif isinstance(partner, Hoard):
            for zombie in partner._zombies:
                addZombie(zombie)
        else:
            print "You can't make a hoard with that!"


    # TODO: Add combine, account for 2 hoards