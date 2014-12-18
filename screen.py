#############################################################
# 
# The Screen
#
# This class handles anything that needs to be displayed
# This includes the displayed screen along with the hub



from graphics import *
from util import *
import math
from zombie import *

class Screen (object):
    def __init__ (self,level,window,cx,cy):
        self._level = level
        self._window = window
        self._cx = cx 
        self._cy = cy   
        self._texts = []
        bg = Rectangle(Point(-20,-20),Point(WINDOW_WIDTH+20,WINDOW_HEIGHT+20))
        bg.setFill("black")
        bg.setOutline("black")
        bg.draw(window)
        self._current = []
        self._hub = "Default"
        self._dialogue = "talk"
        self._buttons = []
        self._bText = []
        self._dButtons = []
        self._dExtra = []

# A helper function that takes a button name and a position
# to display it on and creates a button
    def makeButton(self, text, pos, part):
        start = 2*TILE_SIZE
        xLeft = WINDOW_WIDTH+TILE_SIZE
        xRight = WINDOW_WIDTH+WINDOW_RIGHTPANEL-TILE_SIZE
        xMid = WINDOW_WIDTH+0.5*WINDOW_RIGHTPANEL

        button =  Rectangle(Point(xLeft,start+((3*pos+1)*part)),Point(xRight,start+(3*pos+3)*part))
        buttonText = Text(Point(xMid, start+(3*pos+2)*part), text)
        self._buttons.append(button)
        self._bText.append(buttonText)
        button.setFill("grey")
        button.draw(self._window)
        buttonText.draw(self._window)

# makeDialogue creates the appropriate dialogue depending on what has been selected
# This can be information about things selected on the map
# It can also be the sell,buy and heal functionality of the NPC
    def makeDialogue(self, status, name, knowledge, items):
        name = Text(Point(100,WINDOW_HEIGHT+37), name.capitalize() + " says:")
        bubble = Rectangle(Point(20, WINDOW_HEIGHT + 20), Point(WINDOW_HEIGHT-20, WINDOW_WIDTH+180))
        ok = Rectangle(Point(WINDOW_HEIGHT-120, WINDOW_WIDTH+130), Point(WINDOW_HEIGHT-30, WINDOW_WIDTH+170))
        accept = Text(Point(WINDOW_HEIGHT-75, WINDOW_WIDTH+150), "OK")
        bubble.setFill("grey")
        ok.setFill("darkgrey")
        bubble.draw(self._window)
        ok.draw(self._window)
        accept.draw(self._window)
        name.draw(self._window)
        self._dExtra.append(bubble)
        self._dExtra.append(ok)
        self._dExtra.append(accept)
        self._dExtra.append(name)
        if status == "Zombie":
            words = Text(Point(WINDOW_WIDTH/2,WINDOW_WIDTH+80),  knowledge)
            words.draw(self._window)
            self._dExtra.append(words)
            words = Text(Point(WINDOW_WIDTH/2,WINDOW_WIDTH+100), "Health: " + str(items[0]._health))
            words.draw(self._window)
            self._dExtra.append(words)
            words = Text(Point(WINDOW_WIDTH/2,WINDOW_WIDTH+120), "Type: " + items[0]._status.capitalize())
            words.draw(self._window)
            self._dExtra.append(words)
            words = Text(Point(WINDOW_WIDTH/2,WINDOW_WIDTH+140), "Strength: " + str(items[0]._power))
            words.draw(self._window)
            self._dExtra.append(words)
            if len(items[0]._zombies) > 1:
                words = Text(Point(WINDOW_WIDTH/2,WINDOW_WIDTH+160), "Zombies Contained: " + str(len(items[0]._zombies)))
                words.draw(self._window)
                self._dExtra.append(words)
            self._dialogue = "talk"
        if status == "Rat":
            words = Text(Point(WINDOW_WIDTH/2,WINDOW_WIDTH+80),  knowledge)
            words.draw(self._window)
            self._dExtra.append(words)
            words = Text(Point(WINDOW_WIDTH/2,WINDOW_WIDTH+100), "Health: " + str(items[0]._health))
            words.draw(self._window)
            self._dExtra.append(words)
            words = Text(Point(WINDOW_WIDTH/2,WINDOW_WIDTH+120), "Strength: " + str(items[0]._power))
            words.draw(self._window)
            self._dExtra.append(words)
            self._dialogue = "talk"
        if status == "Statue":
            words = Text(Point(WINDOW_WIDTH/2,WINDOW_WIDTH+80), knowledge)
            words.draw(self._window)
            self._dExtra.append(words)
            words = Text(Point(WINDOW_WIDTH/2,WINDOW_WIDTH+100), "Health: " + str(items[0]._health))
            words.draw(self._window)
            self._dExtra.append(words)
            self._dialogue = "talk"
        if status == "NPC":
            words = Text(Point(WINDOW_WIDTH/2,WINDOW_WIDTH+80), "I am a " +  knowledge)
            words.draw(self._window)
            self._dExtra.append(words)
            words = Text(Point(WINDOW_WIDTH/2,WINDOW_WIDTH+100), "Health: " + str(items[0]._health))
            words.draw(self._window)
            self._dExtra.append(words)
            self._dialogue = "talk"
        if status == "feather":
            words = Text(Point(WINDOW_WIDTH/2,WINDOW_WIDTH+80),  knowledge)
            words.draw(self._window)
            self._dExtra.append(words)
            words = Text(Point(WINDOW_WIDTH/2,WINDOW_WIDTH+100), "Uses Remaining: " + str(items[0]._health))
            words.draw(self._window)  
            self._dExtra.append(words)
            self._dialogue = "talk"
        if status == "talk":
            words = Text(Point(WINDOW_WIDTH/2,WINDOW_WIDTH+100), knowledge)
            words.draw(self._window)
            self._dExtra.append(words)
            self._dialogue = "talk"
        elif status == "sell":
            words = Text(Point(200,WINDOW_HEIGHT+60), "yes, what would you like to buy?")
            words.draw(self._window)
            self._dExtra.append(words)
            self._dialogue = "sell"
            for i in range(20):
                posX = 80 + (i%10)*(TILE_SIZE+2)
                posY = WINDOW_HEIGHT + 100  + math.floor(i/10)*(1.5*TILE_SIZE)
                elt = Rectangle(Point(posX, posY), Point(posX+TILE_SIZE-1, posY+TILE_SIZE-1))
                elt.setFill('grey')
                elt.setOutline('darkgrey')
                elt.draw(self._window)
                self._dExtra.append(elt)
            for i in range(len(items)):
                items[i]._sprite.draw(self._window)
                thing = items[i]
                thingText = Text(items[i]._sprite.anchor, str(items[i]._price))
                thingText.draw(self._window)
                self._dButtons.append(thing)
                self._dExtra.append(thingText)
        elif status == "heal":
            words = Text(Point(200,WINDOW_HEIGHT+60), "Well, nothing comes free you know...")
            words.draw(self._window)
            self._dExtra.append(words)
            self._dialogue = "heal"


# MakeHub calls makeButton for all buttons needed in the current menu
# There are 3 possible menus - directing friendly zombies, interacting with gravestones
# and talking to NPCs
    def makeHub(self, selected):
        part = (WINDOW_HEIGHT - 2*TILE_SIZE)/16
        for i in range(len(self._buttons)):
            self._buttons[i].undraw()
            self._bText[i].undraw()
        self._buttons = []
        self._bText = []  
        if self._hub == "Friend":
            self.makeButton("Walk", 0, part)
            self.makeButton("Attack", 1, part)
            self.makeButton("Follow", 2, part)
            self.makeButton("Group", 3, part)
        if self._hub == "Gravestone":
            self.makeButton("Rise Up", 0, part)
        if self._hub == "NPC":
            self.makeButton("Talk", 0, part)
            self.makeButton("Buy", 1, part)
            self.makeButton("Heal", 2, part)

# Text that is displayed on the board needs to be tracked
# so that it can later be removed when the event queue is popped
# Example when characters are hit and yell "Squee"
    def addText(self,text):
        self._texts.append((text,0))

# Function called by the event queue
# It removes any old text on the window
    def event(self,q):
        undrawList = [x for x in self._texts if x[1] > 50]
        self._texts[:] = [x for x in self._texts if x[1] <= 50]
        for text,age in undrawList:
            text.undraw()
        for i in range(len(self._texts)):
            self._texts[i] = (self._texts[i][0], self._texts[i][1] + 1)
        self.register(q,1)

# Registers the Screen back into the event queue
    def register (self,q,freq):
        self._freq = freq
        q.enqueue(freq,self)
        return self

# This handles any movement needed by the screen itself based on changes made by the player. 
    def move(self, dx, dy):
        vX = VIEWPORT_WIDTH-1
        vY = VIEWPORT_HEIGHT-1
        for tile in self._current:
            tile.move(-dx*TILE_SIZE,-dy*TILE_SIZE)
            if tile.anchor.x < 0 and tile.anchor.x/TILE_SIZE +1 > VIEWPORT_WIDTH and tile.anchor.y < 0 and title.anchor.y/TILE_SIZE + 1 > VIEWPORT_HEIGHT:
                tile.undraw()
                self._current.remove(tile)

# Finds the appropriate image needed for each terain type
    def find_images(self,x,y):
        if self.tile(x,y) == 0:
            return 'lightGrassBrown.gif'
        elif self.tile(x,y) == 1:
            return 'grassBrown.gif'
        elif self.tile(x,y) == 2:
            return 'treeBrown.gif'
        elif self.tile(x,y) == 3:
            return 'wall.gif'

# moves the screen to display the correct starting screen
    def init_move(self, cy, cx):
        dx = (VIEWPORT_WIDTH-1)/2
        dy = (VIEWPORT_HEIGHT-1)/2
        for y in range(LEVEL_HEIGHT):
            for x in range(LEVEL_WIDTH):
                sx = (x-(cx-dx)) * TILE_SIZE
                sy = (y-(cy-dy)) * TILE_SIZE
                elt = Image(Point(sx+TILE_SIZE/2,sy+TILE_SIZE/2),self.find_images(x,y))
                self._current.append(elt)
                elt.draw(self._window)
        self.move(0,0)

# Returns the tile at the corresponding position
    def tile (self,x,y):
        return self._level.tile(x,y)

# Adds the object sprites to the screen
    def add (self,item,x,y):
        if isinstance(item, Zombie):
            item._sprite2.move((x-(self._cx-(VIEWPORT_WIDTH-1)/2))*TILE_SIZE,(y-(self._cy-(VIEWPORT_HEIGHT-1)/2))*TILE_SIZE)
            item._sprite2.draw(self._window)   
            item._sprite1.move((x-(self._cx-(VIEWPORT_WIDTH-1)/2))*TILE_SIZE,(y-(self._cy-(VIEWPORT_HEIGHT-1)/2))*TILE_SIZE)
            item._sprite1.draw(self._window)          
        item.sprite().move((x-(self._cx-(VIEWPORT_WIDTH-1)/2))*TILE_SIZE,(y-(self._cy-(VIEWPORT_HEIGHT-1)/2))*TILE_SIZE)
        item.sprite().draw(self._window)

# Getter method for the screen's window
    def window (self):
        return self._window


