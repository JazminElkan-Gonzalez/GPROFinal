from util import *
from zombie import *
from npc import *
from rat import *
from feather import *

class CheckInput (object):
    def __init__ (self,window,player):
        self._player = player
        self._window = window
        self._buttonState = None
        self._selected = None

    def findObject(self, mouse, objList):
        for i in range(len(objList)):
            if isinstance(objList[i]._sprite, Image):
                xLeft = objList[i]._sprite.getAnchor().x - TILE_SIZE/2
                yLeft = objList[i]._sprite.getAnchor().y - TILE_SIZE/2
            else:
                xLeft = objList[i]._sprite.p1.x
                yLeft = objList[i]._sprite.p1.y
            if mouse.x > xLeft and mouse.x < xLeft + TILE_SIZE and mouse.y > yLeft and mouse.y < yLeft + TILE_SIZE:
                return objList[i]

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
                self._player._screen._hub = "Default"
            elif isinstance(found, Zombie):
                self._player._screen.makeDialogue("Zombie", found._name, found._description, [found])
                if found._status == "gravestone":
                    self._player._screen._hub = "Gravestone"
                if found._status == "friend":
                    self._player._screen._hub = "Friend"
            elif isinstance(found, NPC):
                if abs(mouse.x-self._player._sprite.anchor.x) <= 3*TILE_SIZE and abs(mouse.y-self._player._sprite.anchor.y) <= 3*TILE_SIZE:
                    self._player._screen._hub = "NPC"
                else:
                    words  = Text(Point(WINDOW_WIDTH/2,WINDOW_WIDTH+100), "Too Far Away!")
                    words.draw(self._player._screen._window)
                    self._player._screen.addText(words)
            elif isinstance(found, Feather):
                self._player._screen.makeDialogue("talk", found._name, found._description, [])
                self._player.pickup(found)
                self._player._screen._hub = "Default"
                self._selected = None
        else:
            self._player._screen._hub = "Default"
            self._selected = None
        self._player._screen.makeHub(self._selected)

    def buttonPress(self, mouse):
        part = (WINDOW_HEIGHT - 2*TILE_SIZE)/16
        xLeft = WINDOW_WIDTH+TILE_SIZE
        xRight = WINDOW_WIDTH+WINDOW_RIGHTPANEL-TILE_SIZE
        for i in range(len(self._player._screen._buttons)):
            yLeft = self._player._screen._buttons[i].p1.y
            if mouse.x > xLeft and mouse.x < xRight and mouse.y > yLeft and mouse.y < yLeft + 2*part:
                if self._player._screen._hub == "Friend":
                    if i == 4: #mode
                        self._player._screen._hub = "Default"
                        self._selected = None
                        self._player._screen.makeHub(self._selected)
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
                        self._selected = None
                        self._player._screen.makeHub(self._selected)
                    break
                elif self._player._screen._hub == "Gravestone":
                    self._selected.wakeUp()
                    self._player._screen._hub = "Default"
                    self._selected = None
                    self._player._screen.makeHub(self._selected)
                    break

    def clickPos(self, mouse):
            return mouse.x/TILE_SIZE-10+self._player._x, mouse.y/TILE_SIZE-10+self._player._y

    def thirdClick(self, mouse):
        if self._buttonState == "Walk":
            self._selected._movement = "walkTo"
            self._selected._walkToX, self._selected._walkToY = self.clickPos(mouse)
        elif self._buttonState == "Attack":
            self._selected._movement = "attack"
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
                    rect = Rectangle(bought._sprite.p1, bought._sprite.p2)
                    rect.setFill('grey')
                    rect.setOutline('darkgrey')
                    rect.draw(self._window)
                    self._player._screen._dExtra.append(rect)
                    bought._user.sold(bought, self._player)

    def inventoryClick(self, mouse):
        found = self.findObject(mouse, self._player._items)
        if isinstance(found, Feather):
            self._buttonState = "Feather"
            self._selected = found  
            self._player._screen.makeDialogue("feather", found._name, found._description, [found])  

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
