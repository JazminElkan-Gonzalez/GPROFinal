#############################################################
# 
# A function that expands on Character functionality
# The Rat has not changed much from its original functionality. 



from character import *
import time
from player import *
from zombie import *

class Rat (Character):
    def __init__ (self,name,desc, health):
        Character.__init__(self,name,desc, health, [])
        pic = random.choice(['rat.gif', 'rat2.gif'])
        self._sprite = Image(Point(TILE_SIZE/2,TILE_SIZE/2),pic)

        self._direction = random.randrange(4)
        self._power = 5

# Gets called when the rat event comes up
# The rat walks in a random direction and then attacks
    def event (self,q):
        if self._dead == False:
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
            self.register(q,self._freq)

# The attack function is called by the event pop
# Rats only attack players and their zombies within one square of them       
    def attack(self):
        for thing in OBJECTS:
            if (self._x - 1 <= thing._x <= self._x + 1) and (self._y - 1 <= thing._y <= self._y + 1) and (thing != self) and (isinstance(thing, Player) or (isinstance(thing, Zombie) and thing._status == "friend")):
                thing.updateHealth(-self._power)
