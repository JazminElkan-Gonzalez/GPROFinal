#############################################################
# 
# A function that handles all inputs from the user
#
# There are tow major ways of interacting with the world
# 
# The keyboard W,A,S,D allows the player to move around 
# 
# Clicking is used for all other interactions
# To diect zombies the player selects the zombie, clicks a "button"
# indicating the command and then selects the target of that command
# 
# Whenever a person clicks on a thing, a dialogue box appears describing that thing
# buttons also appear if there are options
# 
# When interacting with the store clerk the player can click on the dialogue box to interact appropriately 

from util import *
from zombie import *
from npc import *
from rat import *
from feather import *
from status import *

class CheckInput (object):
    def __init__ (self,window,player):
        self._player = player
        self._window = window
        self._buttonState = None
        self._selected = None

# A helper function that checks to see if there is an object at a given location. 
    def findObject(self, mouse, objList):
        for i in range(len(objList)):
            xLeft = objList[i]._sprite.getAnchor().x - TILE_SIZE/2
            yLeft = objList[i]._sprite.getAnchor().y - TILE_SIZE/2
            if mouse.x > xLeft and mouse.x < xLeft + TILE_SIZE and mouse.y > yLeft and mouse.y < yLeft + TILE_SIZE:
                return objList[i]

# This function is used does a few things after finding what objects have been selected
# It checks if the player is close enough to interact with the given object
# It creates a dialogue with the information of the selected object
# It creats buttons with the appropriate options
    def firstClick(self, mouse):
        found = self.findObject(mouse, OBJECTS)
        self._selected = found
        for item in self._player._screen._dButtons:
            item._sprite.undraw()
        for item in self._player._screen._dExtra:
            item.undraw()
        self._player._screen._dButtons = []
        self._player._screen._dExtra = []
        if found != None:
            if isinstance(found, Rat):
                if abs(mouse.x-self._player._sprite.anchor.x) <= 5*TILE_SIZE and abs(mouse.y-self._player._sprite.anchor.y) <= 5*TILE_SIZE:
                    self._player._screen._hub = "Default"
                    self._player._screen.makeDialogue("Rat", found._name, found._description, [found])
                else:
                    words  = Text(Point(WINDOW_WIDTH/2,WINDOW_WIDTH+100), "Too Far Away!")
                    words.draw(self._player._screen._window)
                    self._player._screen.addText(words)
                    self._player._screen._hub = "Default"
                    self._selected = None
            elif isinstance(found, Zombie):
                if abs(mouse.x-self._player._sprite.anchor.x) <= 5*TILE_SIZE and abs(mouse.y-self._player._sprite.anchor.y) <= 5*TILE_SIZE:
                    self._player._screen.makeDialogue("Zombie", found._name, found._description, [found])
                    if found._status == "gravestone":
                        self._player._screen._hub = "Gravestone"
                    if found._status == "friend":
                        self._player._screen._hub = "Friend"
                else:
                    words  = Text(Point(WINDOW_WIDTH/2,WINDOW_WIDTH+100), "Too Far Away!")
                    words.draw(self._player._screen._window)
                    self._player._screen.addText(words)
                    self._player._screen._hub = "Default"
                    self._selected = None
            elif isinstance(found, Feather):
                if abs(mouse.x-self._player._sprite.anchor.x) <= 3*TILE_SIZE and abs(mouse.y-self._player._sprite.anchor.y) <= 3*TILE_SIZE:
                    self._player._screen.makeDialogue("feather", found._name, found._description, [found])
                    self._player.pickup(found)
                    self._player._screen._hub = "Default"
                    self._selected = None    
                else:
                    words  = Text(Point(WINDOW_WIDTH/2,WINDOW_WIDTH+100), "Too Far Away!")
                    words.draw(self._player._screen._window)
                    self._player._screen.addText(words)
                    self._player._screen._hub = "Default"
                    self._selected = None
            elif isinstance(found, OlinStatue):
                if abs(mouse.x-self._player._sprite.anchor.x) <= 3*TILE_SIZE and abs(mouse.y-self._player._sprite.anchor.y) <= 3*TILE_SIZE:
                    self._player._screen.makeDialogue("Statue", found._name, found._description, [found])
                    self._player._screen._hub = "Default"
                    self._selected = None    
                else:
                    words  = Text(Point(WINDOW_WIDTH/2,WINDOW_WIDTH+100), "Too Far Away!")
                    words.draw(self._player._screen._window)
                    self._player._screen.addText(words)
                    self._player._screen._hub = "Default"
                    self._selected = None
            elif isinstance(found, NPC):
                if abs(mouse.x-self._player._sprite.anchor.x) <= 3*TILE_SIZE and abs(mouse.y-self._player._sprite.anchor.y) <= 3*TILE_SIZE:
                    self._player._screen.makeDialogue("NPC", found._name, found._description, [found]) 
                    self._player._screen._hub = "NPC"
                else:
                    words  = Text(Point(WINDOW_WIDTH/2,WINDOW_WIDTH+100), "Too Far Away!")
                    words.draw(self._player._screen._window)
                    self._player._screen.addText(words)
                    self._player._screen._hub = "Default"
                    self._selected = None         
        else:
            self._player._screen._hub = "Default"
            self._selected = None
        self._player._screen.makeHub(self._selected)

# Once the player has selected one of the buttons representing the options
# This function finds the option that has been pressed and calls the appropriate functions. 
    def buttonPress(self, mouse):
        part = (WINDOW_HEIGHT - 2*TILE_SIZE)/16
        xLeft = WINDOW_WIDTH+TILE_SIZE
        xRight = WINDOW_WIDTH+WINDOW_RIGHTPANEL-TILE_SIZE
        for i in range(len(self._player._screen._buttons)):
            yLeft = self._player._screen._buttons[i].p1.y
            if mouse.x > xLeft and mouse.x < xRight and mouse.y > yLeft and mouse.y < yLeft + 2*part:
                self._player._screen._buttons[i].setFill('darkgray')
                if self._player._screen._hub == "Friend":
                    if i == 2: #follow
                        self._selected._movement = "follow"
                        self._player._screen._hub = "Default"
                        self._selected = None
                        self._player._screen.makeHub(self._selected)  
                    else:
                        self._buttonState = ZOMBIEBUTT[i]
                    break
                elif self._player._screen._hub == "NPC":
                    if i == 0: #talk
                        self._player._screen._hub = "Default"
                        self._selected.talk()
                        self._selected = None
                        self._player._screen.makeHub(self._selected)
                    if i == 1: #sell
                        self._player._screen._hub = "Default"
                        self._selected.sell()
                        self._selected = None
                        self._player._screen.makeHub(self._selected)
                    if i == 2: #heal
                        self._player._screen._hub = "Default"
                        self._selected.heal()
                        self._player.changeGold(-10)
                        self._selected = None
                        self._player._screen.makeHub(self._selected)
                    break
                elif self._player._screen._hub == "Gravestone":
                    self._selected.wakeUp()
                    self._player._screen._hub = "Default"
                    self._selected = None
                    self._player._screen.makeHub(self._selected)
                    break

# Some commands need a "target". refered to as the "third click"
# Once the target has been found, this function calls the appropriate functions
    def thirdClick(self, mouse):
        if self._buttonState == "Walk":
            self._selected._movement = "walkTo"
            self._selected._walkToX, self._selected._walkToY = mouse.x/TILE_SIZE-10+self._player._x, mouse.y/TILE_SIZE-10+self._player._y
        elif self._buttonState == "Attack":
            self._selected.setAttack(self.findObject(mouse, OBJECTS))
        elif self._buttonState == "Group":
            self._selected.combine(self.findObject(mouse, OBJECTS))
        elif self._buttonState == "Feather":
            found = self.findObject(mouse, OBJECTS)
            if isinstance(found, Zombie):
                found.updateHealth(5)
                self._selected.use()
        else:
            pass
        self._buttonState = None
        self._selected = None
        self._player._screen._hub = "Default"
        self._player._screen.makeHub(self._selected)


# This function is used in the case that the player is interacting with the dialogue
# If the player hits "ok" in the lower corner, the dialogue closes and complete the appropriate action
# The player can also use the dialogue to buy items from the blacksmith 
    def textClick(self,mouse):
        if mouse.x >= WINDOW_HEIGHT-120:
            if self._player._screen._dialogue == "heal":
                self._player.updateHealth(self._player._maxHealth - self._player._health)
            for item in self._player._screen._dButtons:
                item._sprite.undraw()
            for item in self._player._screen._dExtra:
                item.undraw()
            self._player._screen._dButtons = []
            self._player._screen._dExtra = []
        else:
            bought = self.findObject(mouse, self._player._screen._dButtons)
            if bought != None:
                if bought._price <= self._player._gold:
                    rect = Rectangle(Point(bought._sprite.anchor.x - (TILE_SIZE/2),bought._sprite.anchor.y-(TILE_SIZE/2)),Point(bought._sprite.anchor.x + (TILE_SIZE/2),bought._sprite.anchor.y+(TILE_SIZE/2)))
                    rect.setFill('grey')
                    rect.setOutline('darkgrey')
                    rect.draw(self._window)
                    self._player._screen._dExtra.append(rect)
                    bought._user.sold(bought, self._player)

# This is used when the player clicks on their inventory
# It finds the selected item, tells the user what the item is and then waits for the target
    def inventoryClick(self, mouse):
        found = self.findObject(mouse, self._player._items)
        if isinstance(found, Feather):
            self._buttonState = "Feather"
            self._selected = found  
            self._player._screen.makeDialogue("feather", found._name, found._description, [found])  

# This is the header function that finds what step the player is on in terms of what he/she is trying to do 
    def event (self,q):
        key = self._window.checkKey()
        mouse = self._window.checkMouse()
        if mouse != None:
            if mouse.x < WINDOW_WIDTH and mouse.y < WINDOW_HEIGHT:
                if self._buttonState == None:
                    self.firstClick(mouse)
                else:
                    self.thirdClick(mouse)
            if mouse.y >= WINDOW_HEIGHT and mouse.x >= WINDOW_WIDTH:
                self.inventoryClick(mouse)
            elif mouse.x >= WINDOW_WIDTH:
                self.buttonPress(mouse)
            elif mouse.y >= WINDOW_HEIGHT:
                self.textClick(mouse)
        if key == 'q':
            self._window.close()
            exit(0)
        if key in MOVE:
            (dx,dy) = MOVE[key]
            self._player.move(dx,dy)
        q.enqueue(1,self)
