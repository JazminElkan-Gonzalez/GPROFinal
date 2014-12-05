from util import *
from zombie import *
from npc import *
from rat import *
class CheckInput (object):
    def __init__ (self,window,player):
        self._player = player
        self._window = window
        self._buttonState = None

    def event (self,q):
        key = self._window.checkKey()
        mouse = self._window.checkMouse()
        if mouse != None:
            if mouse.x < WINDOW_WIDTH:
                if self._buttonState == None:
                    for i in range(len(OBJECTS)):
                        if isinstance(OBJECTS[i]._sprite, Image):
                            xLeft = OBJECTS[i]._sprite.getAnchor().x - TILE_SIZE/2
                            yLeft = OBJECTS[i]._sprite.getAnchor().y - TILE_SIZE/2
                        else:
                            xLeft = OBJECTS[i]._sprite.p1.x
                            yLeft = OBJECTS[i]._sprite.p1.y
                        if mouse.x > xLeft and mouse.x < xLeft + TILE_SIZE and mouse.y > yLeft and mouse.y < yLeft + TILE_SIZE:
                            selected = OBJECTS[i]
                            if isinstance(OBJECTS[i], Rat):
                                self._player._screen._hub = "Default"
                            elif isinstance(OBJECTS[i], Zombie):
                                self._player._screen._hub = "Zombie"
                            elif isinstance(OBJECTS[i], NPC):
                                self._player._screen._hub = "NPC"
                            break
                        elif i == len(OBJECTS) -1:
                            self._player._screen._hub = "Default"
                            selected = None
                    self._player._screen.makeHub(selected)
                elif self._buttonState == "Walk":
                    self._buttonState = None 
            if mouse.x >= WINDOW_WIDTH:
                pass


        if key == 'q':
            self._window.close()
            exit(0)
        if key in MOVE:
            (dx,dy) = MOVE[key]
            self._player.move(dx,dy)

        q.enqueue(1,self)
