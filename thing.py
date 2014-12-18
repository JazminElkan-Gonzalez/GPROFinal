#############################################################
# 
# A Parent object for all Things in the game
# Things have a description, a name and health

from root import *
from graphics import *
from util import *

class Thing (Root):
    def __init__ (self,name,desc, health):
        self._name = name
        self._description = desc
        self._health = health
        self._sprite = Text(Point(TILE_SIZE/2,TILE_SIZE/2),"?")
        self._dead = False

    def __str__ (self):
        return "<"+self.name()+">"

# Allows things to be added to the event queue
    def register (self,q,freq):
        self._freq = freq
        q.enqueue(freq,self)
        return self

# Moves the sprite to a given location
    def moveSprite(self,x,y):
        self._sprite.move(x,y)

# A simple walk function
# Checks to see if it is able to move in a given location
    def walk(self, dx, dy):
        nx = self._x + dx
        ny = self._y + dy
        if self._screen.tile(nx,ny) == 0 or self._screen.tile(nx,ny) == 1:
            self._y = ny
            self._x = nx
            self.moveSprite(dx*TILE_SIZE,dy*TILE_SIZE)

# When the thing is attacked or healed, his or her health needs to be changed
# The thing also yells out and adds his text to a list that gets removed every so often
    def updateHealth(self, amount):
        if self._health > 0:
            self._health = self._health + amount
            words = Text(self._sprite.anchor, "SQUEE")
            words.draw(self._screen._window)
            self._screen.addText(words)
            if self._health <= 0:
                self.die()

# when a thing dies it removes itself from the world object list and undraws itself
    def die(self):
        self._dead = True
        OBJECTS.remove(self)
        self._sprite.undraw()


# return the sprite for display purposes
    def sprite (self):
        return self._sprite

# return the name
    def name (self):
        return self._name

# return the position of the thing in the level array
    def position (self):
        return (self._x,self._y)
        
# return the description
    def description (self):
        return self._description

# Changes the position of the thing based on the movement of the player
    def update_pos(self, dx, dy):
        vX = VIEWPORT_WIDTH-1
        vY = VIEWPORT_HEIGHT-1
        self.moveSprite(-dx*TILE_SIZE,-dy*TILE_SIZE)
        # self.antiDraw()


# creating a thing does not put it in play -- you have to 
# call materialize, passing in the screen and the position
# where you want it to appear
    def materialize (self,screen,x,y):
        OBJECTS.append(self)
        self._screen = screen
        self._x = x
        self._y = y
        return self

# A quick tag to indicate that the object is a thing
    def is_thing (self):
        return True

# Indicates that you cannot walk through this object
    def is_walkable (self):
        return False