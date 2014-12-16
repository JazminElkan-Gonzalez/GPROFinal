from root import *
from graphics import *
from util import *

class Thing (Root):
    def __init__ (self,name,desc, health):
        self._name = name
        self._description = desc
        self._health = health
        self._sprite = Text(Point(TILE_SIZE/2,TILE_SIZE/2),"?")
        log("Thing.__init__ for "+str(self))

    def __str__ (self):
        return "<"+self.name()+">"


    def register (self,q,freq):
        self._freq = freq
        q.enqueue(freq,self)
        return self

    def walk(self, dx, dy):
        nx = self._x + dx
        ny = self._y + dy
        if self._screen.tile(nx,ny) == 0 or self._screen.tile(nx,ny) == 1:
            self._y = ny
            self._x = nx
            self._sprite.move(dx*TILE_SIZE,dy*TILE_SIZE)
            self.antiDraw()


    def antiDraw(self):
        if isinstance(self._sprite, Image):
            xLeft = self._sprite.getAnchor().x - TILE_SIZE/2
            yLeft = self._sprite.getAnchor().y - TILE_SIZE/2
            if xLeft < 0 and xLeft/TILE_SIZE +1 > VIEWPORT_WIDTH and yLeft < 0 and yLeft/TILE_SIZE + 1 > VIEWPORT_HEIGHT:
                self._sprite.undraw()        
        else:            
            if self._sprite.p1.x < 0 and self._sprite.p1.x/TILE_SIZE +1 > VIEWPORT_WIDTH and self._sprite.p1.y < 0 and self._sprite.p1.y/TILE_SIZE + 1 > VIEWPORT_HEIGHT:
                self._sprite.undraw()        

    def updateHealth(self, amount):
        if self._health > 0:
            print self._name,  "lost health: ", self._health
            self._health = self._health + amount
            if isinstance(self._sprite, Image):
                words = Text(self._sprite.anchor, "SQUEE")
            else:
                words = Text(self._sprite.p1, "SQUEE")
            # words = Text(self._sprite.p1, "SQUEE")
            words.draw(self._screen._window)
            self._screen.addText(words)
            if self._health <= 0:
                self.die()

    def die(self):
        self._dead = True
        OBJECTS.remove(self)
        self._sprite.undraw()
        print self._name + "has died"


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

    def update_pos(self, dx, dy):
        vX = VIEWPORT_WIDTH-1
        vY = VIEWPORT_HEIGHT-1
        self._sprite.move(-dx*TILE_SIZE,-dy*TILE_SIZE)
        self.antiDraw()


    # creating a thing does not put it in play -- you have to 
    # call materialize, passing in the screen and the position
    # where you want it to appear
    def materialize (self,screen,x,y):
        OBJECTS.append(self)
        screen.add(self,x,y)
        self._screen = screen
        self._x = x
        self._y = y
        return self

    def is_thing (self):
        return True

    def is_walkable (self):
        return False