from util import *
from character import *
from npc import *
from player import *

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
        rect.setFill("grey")
        rect.setOutline("black")
        self._sprite = rect

        self._status = "gravestone"
        self._movement = "enemy"
        # self._movement = "attack"
        # self._attackObject

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

    #Zombie will walk towards a position on the screen determined by otherX, otherY
    #TODO: make it so zombies can walk around obstructions
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
        isObj = False
        sightRange = 7
        if self._status != "gravestone":
            #enemy movements
            if self._movement == "enemy":
                enemySpotted = False
                for i in range(len(OBJECTS)):
                    if isinstance(OBJECTS[i], NPC) or isinstance(OBJECTS[i], Player):
                        for x in range(-sightRange,sightRange+1):
                            for y in range(-sightRange,sightRange+1):
                                if OBJECTS[i]._x == self._x + x and OBJECTS[i]._y == self._y + y:
                                    enemySpotted = True
                                    newX, newY = self.walkTo(OBJECTS[i]._x, OBJECTS[i]._y)
                if enemySpotted == False:
                    newX, newY = random.randint(0,1),random.randint(0,1)



            # if self._movement == "wander":  #enemy movement only
            #     #TODO: make this work properly, enemies!! so that it'll attack you if you're close or npcs are cose
            #     newX, newY = random.randint(0,1),random.randint(0,1)
            # if self._movement == "enemyAttack":

            
            #friend movements
            if self._movement == "follow":
                newX, newY = self.followPlayer()
            if self._movement == "walkTowards":
                newX, newY = self.walkTo(self._walkToX, self._walkToY)
            # if self._movement == "attack":

            for i in range(len(OBJECTS)):
                if OBJECTS[i]._x == self._x + newX and OBJECTS[i]._y == self._y + newY:
                    isObj = True
                    if OBJECTS[i].is_walkable():
                        self.walk(newX, newY)
            if isObj == False:
                self.walk(newX,newY)
            
            if self._status == "enemy": #add attack mode for friendies
                self.attack()

        self.register(q,self._freq)

    def attack(self):
        if self._status == "gravestone":
            pass
        elif self._status == "enemy":
            positions = [(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1)]
            for thing in OBJECTS:
                if thing != self:
                    for adj in positions:
                        if (thing._x == self._x + adj[0] and thing._y == self._y + adj[1]):
                    # if (thing._x == self._x and thing._y == self._y -1) or (thing._x == self._x and thing._y == self._y + 1) or  (thing._x == self._x + 1 and thing._y == self._y) or  (thing._x == self._x - 1 and thing._y == self._y) or (thing._x == self._x and thing._y == self._y):
                            thing.updateHealth(-5)

