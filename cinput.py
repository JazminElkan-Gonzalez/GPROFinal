from util import *

class CheckInput (object):
    def __init__ (self,window,player):
        self._player = player
        self._window = window

    def event (self,q):
        key = self._window.checkKey()
        if key == 'q':
            self._window.close()
            exit(0)
        if key in MOVE:
            (dx,dy) = MOVE[key]
            self._player.move(dx,dy)

        q.enqueue(1,self)
