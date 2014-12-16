from util import *
from character import *
from npc import *
from player import *

class Zombie (Character):
    def __init__ (self,name,desc,health):
        Character.__init__(self,name,desc,health, [])
        log("Zombie.__init__ for "+str(self))
        rect = Rectangle(Point(1,1),
                         Point(TILE_SIZE-1,TILE_SIZE-1))
        rect.setFill("grey")
        rect.setOutline("black")
        self._sprite = rect

        pic = 'zombie2.gif'
        self._sprite = Image(Point(TILE_SIZE/2,TILE_SIZE/2),pic)

        
        self._power = 5
        self._origHealth = health
        self._zombies = [self]
        self._dead = False

        self._status = "gravestone"
        self._movement = "enemy"
        # self._movement = "attack"
        # self._attackObject

    def move(self,newX,newY):
        print self._x, self._y

    def wakeUp(self):
        if self._status == "gravestone":
            self._status = "enemy"
            if isinstance(self._sprite, Rectangle):
                self._sprite.setFill("darkgreen")
                self._sprite.setOutline("red")
            for thing in OBJECTS:
                if thing.is_player():
                    self.player = thing
            self.die()  #temporary to test friend functionality
        else:
            words = Text(self._sprite.p1, "GRR")
            words.draw(self._screen._window)
            self._screen.addText(words)

    def die(self):
        if self._status == "enemy":
            self._status = "friend"
            self._movement = "follow"
            if isinstance(self._sprite, Rectangle):
                self._sprite.setOutline("green")
            self._health = self._origHealth
        # elif self._status == "friend":
        #     self.die()
        #     self._dead = True
        elif self._status == "hoard" or self._status == "friend": 
            OBJECTS.remove(self)
            self._sprite.undraw()
            self._status = "friend"
            self._dead = True

    def zombieNum(self):
        return len(self._zombies)

    def addZombieStats(self,zombie):
        # self._zombies.append(zombie)
        self._health = self._health + zombie._health
        self._power = self._power + zombie._power
        # self._freq = self._freq + 20

    def combine(self,partner):
        if isinstance(partner, Zombie) and partner != self:
            if len(partner._zombies) > 1:
                for zom in partner._zombies:
                    self._zombies.append(zom)
            else:
                self._zombies.append(partner)
            self.addZombieStats(partner)
            self._freq = 7*len(self._zombies)+100
            
            if isinstance(self._sprite, Rectangle):
                self._sprite.setOutline("yellow")
            
            partner._status = "hoard"
            partner._power = 0
            partner.die()
        else:
            print "You can't make a hoard with that!"


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

    def setAttack(self,attackObject):
        self._attackObject = attackObject
        self._movement = "attack"

    def updateHealth(self, amount):
        print self._name, "'s health: ", self._health
        if self._status == "gravestone":
            return
        self._health = self._health + amount
        if isinstance(self._sprite, Image):
            words = Text(self._sprite.anchor, "SQUEE")
        else:
            words = Text(self._sprite.p1, "SQUEE")
        words.draw(self._screen._window)
        self._screen.addText(words)
        if self._health == 0:
            self.die()

    def event (self,q):
        isObj = False
        sightRange = 8
        if self._status != "gravestone":
            #enemy movements
            if self._movement == "enemy":
                enemySpotted = False
                for i in range(len(OBJECTS)):
                    if isinstance(OBJECTS[i], NPC) or isinstance(OBJECTS[i], Player):
                        if (self._x - sightRange < OBJECTS[i]._x < self._x + sightRange) and (self._y - sightRange < OBJECTS[i]._y < self._y + sightRange):
                            enemySpotted = True
                            newX, newY = self.walkTo(OBJECTS[i]._x, OBJECTS[i]._y)
                if enemySpotted == False:
                    newX, newY = random.randint(0,1),random.randint(0,1)
            
            #friend movements
            if self._movement == "follow":
                newX, newY = self.followPlayer()
            if self._movement == "attack":
                newX, newY = self.walkTo(self._attackObject._x, self._attackObject._y)

            for i in range(len(OBJECTS)):
                if OBJECTS[i]._x == self._x + newX and OBJECTS[i]._y == self._y + newY:
                    isObj = True
                    if OBJECTS[i].is_walkable():
                        self.walk(newX, newY)
            if isObj == False:
                self.walk(newX,newY)
            
            self.attack()

        if self._dead == False:
            self.register(q,self._freq)

    def attack(self):
        if self._status == "gravestone" or self._dead == True:
            pass
        else:
            for thing in OBJECTS:
                if thing != self:
                    if (self._x - 1 <= thing._x <= self._x + 1) and (self._y - 1 <= thing._y <= self._y + 1):
                        if not ((thing == self.player or (isinstance(thing,Zombie) and thing._status == "friend")) and self._status == "friend"):
                            thing.updateHealth(-self._power)
                                #TODO: fix that one attacks more than the other
                                #TODO: fix that friendly zombies randomly attack NPCs
