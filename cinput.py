from util import *
from zombie import *
from npc import *
from rat import *
class CheckInput (object):
    def __init__ (self,window,player):
        self._player = player
        self._window = window
        self._buttonState = None
        self._selected = None

    def findObject(self, mouse):
        for i in range(len(OBJECTS)):
            if isinstance(OBJECTS[i]._sprite, Image):
                xLeft = OBJECTS[i]._sprite.getAnchor().x - TILE_SIZE/2
                yLeft = OBJECTS[i]._sprite.getAnchor().y - TILE_SIZE/2
            else:
                xLeft = OBJECTS[i]._sprite.p1.x
                yLeft = OBJECTS[i]._sprite.p1.y
            if mouse.x > xLeft and mouse.x < xLeft + TILE_SIZE and mouse.y > yLeft and mouse.y < yLeft + TILE_SIZE:
                return OBJECTS[i]

    def firstClick(self, mouse):
        found = self.findObject(mouse)
        self._selected = found
        if found != None:
            if isinstance(found, Rat):
                self._player._screen._hub = "Default"
            elif isinstance(found, Zombie):
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

    def thirdClick(self, mouse):
        if self._buttonState == "Walk":
            self._selected._movement = "walkTowards"
            print self._buttonState
            self._selected._walkToX = mouse.x
            self._selected._walkToY = mouse.y
        elif self._buttonState == "Follow":
            self._selected._movement = "follow"
        elif self._buttonState == "Attack":
            self._selected._movement = "attack"
            setAttack(self.findObject(mouse))
        elif self._buttonState == "Group":
            self._selected.combine(self.findObject(mouse))
        else:
            pass
        self._buttonState = None
        self._selected = None
        self._player._screen._hub = "Default"
        self._player._screen.makeHub(self._selected)

    def findInInventory(self, mouse):
        for i in range(len(self._player._screen._dButtons)):
            if isinstance(self._player._screen._dButtons[i]._sprite, Image):
                xLeft = self._player._screen._dButtons[i]._sprite.getAnchor().x - TILE_SIZE/2
                yLeft = self._player._screen._dButtons[i]._sprite.getAnchor().y - TILE_SIZE/2
            else:
                xLeft = self._player._screen._dButtons[i]._sprite.p1.x
                yLeft = self._player._screen._dButtons[i]._sprite.p1.y
            if mouse.x > xLeft and mouse.x < xLeft + TILE_SIZE and mouse.y > yLeft and mouse.y < yLeft + TILE_SIZE:
                return self._player._screen._dButtons[i]

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
            bought = self.findInInventory(mouse)
            if bought != None:
                if bought._price <= self._player._gold:
                    rect = Rectangle(bought._sprite.p1, bought._sprite.p2)
                    rect.setFill('grey')
                    rect.setOutline('darkgrey')
                    rect.draw(self._window)
                    self._player._screen._dExtra.append(rect)
                    bought._user.sold(bought, self._player)



    def event (self,q):
        key = self._window.checkKey()
        mouse = self._window.checkMouse()
        if mouse != None:
            if mouse.x < WINDOW_WIDTH and mouse.y < WINDOW_HEIGHT:
                if self._buttonState == None:
                    self.firstClick(mouse)
                else:
                    self.thirdClick(mouse)
            if mouse.x >= WINDOW_WIDTH:
                self.buttonPress(mouse)
            if mouse.y >= WINDOW_HEIGHT:
                self.textClick(mouse)
        if key == 'q':
            self._window.close()
            exit(0)
        if key in MOVE:
            (dx,dy) = MOVE[key]
            self._player.move(dx,dy)
        q.enqueue(1,self)
