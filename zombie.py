#############################################################
# 
# A function that expands on Character functionality
# A Zombie has 3 sprites of each of its states
# It also has a power indicattion and in some cases, multiple zombies




from util import *
from character import *
from npc import *
from player import *

class Zombie (Character):
    def __init__ (self,name,desc,health):
        Character.__init__(self,name,desc,health, [])

        self._pic = 'gravestone.gif'
        if self._name == "King Prometheus the Green":
            self._pic3 = 'king.gif'
            self._pic2 = 'kingDead.gif'
        else:
            self._pic2 = 'zombie2.gif'
            self._pic3 = 'zombieE.gif'

        self._sprite = Image(Point(TILE_SIZE/2,TILE_SIZE/2),self._pic)
        self._sprite1 = Image(Point(TILE_SIZE/2,TILE_SIZE/2),self._pic3)
        self._sprite2 = Image(Point(TILE_SIZE/2,TILE_SIZE/2),self._pic2)

        
        self._power = health/10
        self._origHealth = health
        self._zombies = [self]

        self._status = "gravestone"
        self._movement = "enemy"
        # self._movement = "attack"
        self._attackObject = None

# Prints to the log that the zombie has moved
    def move(self,newX,newY):
        print self._x, self._y

# Moves all three of the zombies sprites to a given location
    def moveSprite(self,x,y):
        self._sprite.move(x,y)
        self._sprite1.move(x,y)
        self._sprite2.move(x,y)

# Updates the position of the zombie based on the movement of the player
    def update_pos(self, dx, dy):
        vX = VIEWPORT_WIDTH-1
        vY = VIEWPORT_HEIGHT-1
        self.moveSprite(-dx*TILE_SIZE,-dy*TILE_SIZE)

# Walks the zombie to a given location
    def walk(self, dx, dy):
        nx = self._x + dx
        ny = self._y + dy
        if self._screen.tile(nx,ny) == 0 or self._screen.tile(nx,ny) == 1:
            self._y = ny
            self._x = nx
            self.moveSprite(dx*TILE_SIZE,dy*TILE_SIZE)

# When zombie is a gravestone, the player has the option of waking it up
# When the zombie wakes up it is an enemy (unless it is ZOMZOM)
# It undraws the gravestone sprite, displaying the enemy one
    def wakeUp(self):
        if self._status == "gravestone":
            self._status = "enemy"
            self._sprite.undraw()
            for thing in OBJECTS:
                if thing.is_player():
                    self.player = thing
            if self._name == "ZOMZOM":
                self.die()
        else:
            words = Text(self._sprite.p1, "GRR")
            words.draw(self._screen._window)
            self._screen.addText(words)

# When a enemy zombie dies it becomes a friend
# When a friendly zombie dies it gets removed from the world objects and undrawn
    def die(self):
        if self._status == "enemy":
            self._status = "friend"
            self._movement = "follow"
            self._sprite.undraw()
            self._sprite1.undraw()
            self._health = self._origHealth
        elif self._status == "hoard" or self._status == "friend": 
            OBJECTS.remove(self)
            self._sprite2.undraw()
            self._status = "friend"
            self._dead = True
        if self._name == "King Prometheus the Green":
            win(self._screen._window)

# This returns the number of zombies in a hord
    def zombieNum(self):
        return len(self._zombies)

# When Zombies are combined to make a hord
# The zombie power and health is combined
    def addZombieStats(self,zombie):
        self._health = self._health + zombie._health
        self._power = self._power + zombie._power

# This allows the player to combine zombies into more pwerful "hords"
    def combine(self,partner):
        if isinstance(partner, Zombie) and partner != self:
            if len(partner._zombies) > 1:
                for zom in partner._zombies:
                    self._zombies.append(zom)
            else:
                self._zombies.append(partner)
            self.addZombieStats(partner)
            self._freq = 7*len(self._zombies)+14
            self._description = "A zombie hoard!!"
            if "the hoard leader" not in self._name:
                self._name = self._name + " the hoard leader"

            partner._status = "hoard"
            partner._power = 0
            partner.die()
        else:
            print "You can't make a hoard with that!"

# Walks towards the player whenever its event is popped
    def followPlayer(self):
        return self.walkTo(self.player._x, self.player._y)

# Zombie will walk towards a position on the screen determined by otherX, otherY
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

# Sets the object that the zombie is targeting
    def setAttack(self,attackObject):
        if attackObject != None:
            self._attackObject = attackObject
            self._movement = "attack"

# When the zombie is attacked or healed, his or her health needs to be changed
# This updates the values 
# if the zombie health reaches zero, than the die() function is called
    def updateHealth(self, amount):
        if self._status == "gravestone":
            return
        self._health = self._health + amount
        if isinstance(self._sprite, Image):
            words = Text(self._sprite.anchor, "SQUEE")
        else:
            words = Text(self._sprite.p1, "SQUEE")
        words.draw(self._screen._window)
        self._screen.addText(words)
        if self._health <= 0:
            self.die()

# The event funtion is what is called when the Zombie reaches the top
# of the event queue
# Friendly and enemy zombies have different movements
#
# Enemy Zombie:
# If the player is within the detect area of the enemy zombie
# it will try to attack
# Otherwise it will attack NPCs in the area or wander around
#
# Friendly Zombie:
# Depending on the state of the friendly zombie it can do a few things
# Follow the player, attack what is in the area, or walk towards a designated position
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
                if isinstance(self._attackObject, Zombie) and self._attackObject._status == "friend":
                    self._movement = "follow"
                elif self._attackObject._dead == True:
                    self._movement = "follow"
            if self._movement == "walkTo":
                newX, newY = self.walkTo(self._walkToX, self._walkToY)

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

# Attacks anything in range
# If the zombie is friendly then it will only attack enemy zombies or rats or items
# Enemy zombies attack everything
    def attack(self):
        if self._status == "gravestone" or self._dead == True:
            pass
        else:
            for thing in OBJECTS:
                if thing != self:
                    if (self._x - 1 <= thing._x <= self._x + 1) and (self._y - 1 <= thing._y <= self._y + 1):
                        if not ((thing == self.player or (isinstance(thing, NPC) and self._status == "friend" and thing != self._attackObject) or (isinstance(thing,Zombie) and thing._status == "friend")) and self._status == "friend"):
                            thing.updateHealth(-self._power)
                                #TODO: fix that one attacks more than the other

# Adds zombies to the map as gravestones and creates an area of decay around them based on their power level
    def materialize (self,screen,x,y):
        OBJECTS.append(self)
        self._screen = screen
        self._x = x
        self._y = y
        if self._name != "King Prometheus the Green":
            self._screen._level.makeDecay(self._y*LEVEL_WIDTH+self._x, round(self._power/5)+1)
        else:
            self._screen._level.makeDecay(self._y*LEVEL_WIDTH+self._x, 6)

        return self