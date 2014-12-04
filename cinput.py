from util import *
from zombie import *
from npc import *

class CheckInput (object):
    def __init__ (self,window,player):
        self._player = player
        self._window = window

    def event (self,q):
        key = self._window.checkKey()
        mouse = self._window.checkMouse()
        if mouse != None:
            if mouse.x < WINDOW_WIDTH:
                for thing in OBJECTS:
                    if isinstance(thing, Image):
                        xLeft = thing._sprite.getAnchor().x - TILE_SIZE/2
                        yLeft = thing._sprite.getAnchor().y - TILE_SIZE/2
                    else:
                        xLeft = thing._sprite.p1.x
                        yLeft = thing._sprite.p1.y
                    if mouse.x > xLeft and mouse.x < xLeft + TILE_SIZE and mouse.y > yLeft and mouse.y < yLeft + TILE_SIZE:
                            if isinstance(thing, Zombie):
                                self._player._screen._hub = "Zombie"
                            elif isinstance(thing, NPC):
                                self._player._screen._hub = "NPC"
                            break
                self._player._screen.makeHub()


        if key == 'q':
            self._window.close()
            exit(0)
        if key in MOVE:
            (dx,dy) = MOVE[key]
            self._player.move(dx,dy)

        q.enqueue(1,self)
