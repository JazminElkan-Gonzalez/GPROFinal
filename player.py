#############################################################
# 
# A function that expands on Character functionality
# An Player also has gold and a healthBar that is displays on the main hub at all times
# This is where the main functionality of the player comes in



from character import *
from screen import *
import math

class Player (Character):
    def __init__ (self,health,name, items, gold):
        Character.__init__(self,name,"Yours truly", health, items)
        pic = 'necromancer.gif'
        self._sprite = Image(Point(TILE_SIZE/2,TILE_SIZE/2),pic)
        self._healthBar = Rectangle(Point(WINDOW_WIDTH+TILE_SIZE,TILE_SIZE),Point(WINDOW_WIDTH+WINDOW_RIGHTPANEL-TILE_SIZE,2*TILE_SIZE))
        self._gold = gold

# A check method to quickly see what the character is 
    def is_player (self):
        return True

# When the player picks something up, or buys an item it needs to add it to the inventory
# It does this by adding the item to a list and displaying it in the "inventory" section of the hub
    def addInventory(self, item):
        self._items.append(item)
        posX = WINDOW_WIDTH + 20 + ((len(self._items)-1)%5)*(TILE_SIZE+2)
        posY = WINDOW_HEIGHT + 20 + math.floor((len(self._items)-1)/5)*(TILE_SIZE+2)
        item._sprite.move(posX - item._sprite.anchor.x+TILE_SIZE/2, posY - item._sprite.anchor.y+TILE_SIZE/2)

# When the player picks something up from the floor it must remove the item from the world objects list
# It also needs to add it to the inventory of the player
    def pickup(self, item):
        item.pickup(self)
        self.addInventory(item)
        OBJECTS.remove(item)

# When the player finds gold or pays for healing and buying items, gold must be added or removed
# This updates the gold value and draws the appropriate value on the hub
    def changeGold(self, amount):
        self._goldText.undraw()
        self._gold = self._gold + amount
        self._goldText = Text(Point(WINDOW_WIDTH + 100, WINDOW_HEIGHT), "Gold: " + str(self._gold))
        self._goldText.draw(self._screen._window)

# We dont want the character position to be updated since everything is in relation to him
    def update_pos(self, dx, dy):
        pass

# When the player is attacked or healed, his or her health needs to be changed
# This updates the values and redraws the healthbar
# if the player health reaches zero, than the player loses and the game is over
    def updateHealth(self, amount):
        self._health = self._health + amount
        if self._health > 0:
            if isinstance(self._sprite, Image):
                words = Text(self._sprite.anchor, "SQUEE")
            else:
                words = Text(self._sprite.p1, "SQUEE")
            words.draw(self._screen._window)
            self._screen.addText(words)
            self._healthBar.undraw()
            addLength = (WINDOW_RIGHTPANEL - 2*TILE_SIZE)*self._health/self._maxHealth
            self._healthBar = Rectangle(Point(WINDOW_WIDTH+TILE_SIZE,TILE_SIZE),Point(WINDOW_WIDTH+TILE_SIZE + addLength,2*TILE_SIZE))
            self._healthBar.setFill("red")
            self._healthBar.draw(self._screen._window)
            self._preHealth.undraw()
            self._preHealth = Text(Point(WINDOW_WIDTH+1.5*TILE_SIZE,1.5*TILE_SIZE), str(self._health))
            self._preHealth.draw(self._screen._window)

        else:
            self._healthBar.undraw()
            lost(self._screen._window)

# when the player moves it needs to check if the move is valid and then update the position of all other objects
    def move (self,dx,dy):
        nx = self._x + dx
        ny = self._y + dy
        if self._screen.tile(nx,ny) == 0 or self._screen.tile(nx,ny) == 1:
            for i in range(len(OBJECTS)):
                if OBJECTS[i]._x == nx and  OBJECTS[i]._y == ny:
                    if OBJECTS[i].is_walkable():
                        self._y = ny
                        self._x = nx
                        self._screen.move(dx, dy)
                        for thing in OBJECTS:
                            thing.update_pos(dx, dy)
                    break
                elif i == len(OBJECTS) -1:
                    self._y = ny
                    self._x = nx
                    self._screen.move(dx, dy)
                    for thing in OBJECTS:
                        thing.update_pos(dx, dy)


# When the player first materializes, it needs to show the player, and his or her health, gold and inventory
    def materialize (self,screen,x,y):
        OBJECTS.append(self)
        self._screen = screen
        self._x = x
        self._y = y
        self._screen.add(self,self._x,self._y)
        outside = Rectangle(Point(WINDOW_WIDTH+TILE_SIZE,TILE_SIZE),Point(WINDOW_WIDTH+WINDOW_RIGHTPANEL-TILE_SIZE,2*TILE_SIZE))
        outside.setFill("lightgray")
        outside.setOutline("black")
        outside.draw(self._screen._window)
        self._healthBar.setFill("red")
        self._healthBar.draw(self._screen._window)
        self._preHealth = Text(Point(WINDOW_WIDTH+1.5*TILE_SIZE,1.5*TILE_SIZE), str(self._health))
        self._preHealth.draw(self._screen._window)
        self._maxHealth = self._health
        self._goldText = Text(Point(WINDOW_WIDTH + 100, WINDOW_HEIGHT), "Gold: " + str(self._gold))
        self._goldText.draw(self._screen._window)
        for i in range(36):
            posX = WINDOW_WIDTH + 20 + (i%6)*(TILE_SIZE+2)
            posY = WINDOW_HEIGHT + 20 + math.floor(i/6)*(TILE_SIZE+2)
            elt = Rectangle(Point(posX, posY), Point(posX+TILE_SIZE-1, posY+TILE_SIZE-1))
            elt.setFill('grey')
            elt.setOutline('darkgrey')
            elt.draw(self._screen._window)
            if i < len(self._items):
                if isinstance(self._items[i]._sprite, Rectangle):
                    self._items[i]._sprite.move(posX - self._items[i]._sprite.p1.x, posY - self._items[i]._sprite.p1.y)
                elif isinstance(self._items[i]._sprite, Image):
                    self._items[i]._sprite.move(posX - self._items[i]._sprite.getAnchor().x+TILE_SIZE/2, posY - self._items[i]._sprite.getAnchor().y+TILE_SIZE/2)
                self._items[i]._sprite.draw(self._screen._window)         

        return self
