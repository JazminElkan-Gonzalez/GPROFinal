from util import *
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
        # rect.setFill("grey")
        # rect.setOutline("black")
        rect.setFill("darkgreen")
        rect.setOutline("red")
        self._sprite = rect

        self._status = "gravestone"
        self._movement = "follow"


    def move(self,newX,newY):
        print self._x, self._y

    def wakeUp(self):
        if self._status == "gravestone":
            self._status = "enemy"
            self._sprite.setFill("darkgreen")
            self._sprite.setOutline("red")
            for thing in OBJECTS:
                if thing.is_player():
                    self.player = thing
        else:
            words = Text(self._sprite.p1, "GRR")
            words.draw(self._screen._window)
            self._screen.addText(words)

    def followPlayer(self):
        return self.walkTo(self.player._x, self.player._y)

    def randomMove(self):
        return random.randint(0,1),random.randint(0,1)

    #Zombie will walk towards a position on the screen determined by otherX, otherY
    def walkTo(self,otherX,otherY):
        if otherX > self._x:
            newX = 1
        elif otherX == self._x:
            newX = 0
        elif otherX < self._x:
            newX = -1

        if otherY > self._y:
            newY = 1
        elif otherY == self._y:
            newY = 0
        elif otherY < self._y:
            newY = -1

        return newX, newY

    def event (self,q):
        if self._status == "enemy":
            words = self.attack()
            if self._movement == "follow":
                newX, newY = self.followPlayer()
            # newX, newY = self.randomMove()
            self.walk(newX, newY)
            self.attack()
            # log("event for "+str(self))
            self.register(q,self._freq)
        
    def attack(self):
        if self._status == "gravestone":
            pass
        elif self._status == "enemy":
            for thing in OBJECTS:
                if (thing._x == self._x and thing._y == self._y -1) or (thing._x == self._x and thing._y == self._y + 1) or  (thing._x == self._x + 1 and thing._y == self._y) or  (thing._x == self._x - 1 and thing._y == self._y):
                    thing.updateHealth(-5)