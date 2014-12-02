from graphics import *
from util import *
#
# A Screen is a representation of the level displayed in the 
# viewport, with a representation for all the tiles and a 
# representation for the objects in the world currently 
# visible. Managing all of that is key. 
#
# For simplicity, a Screen object contain a reference to the
# level it is displaying, and also to the window in which it
# draws its elements. So you can use the Screen object to 
# mediate access to both the level and the window if you need
# to access them.
# 
# You'll DEFINITELY want to add methods to this class. 
# Like, a lot of them.
#
class Screen (object):
    def __init__ (self,level,window,cx,cy):
        self._level = level
        self._window = window
        self._cx = cx    # the initial center tile position 
        self._cy = cy    #  of the screen
        self._things = []
        # Background is black
        bg = Rectangle(Point(-20,-20),Point(WINDOW_WIDTH+20,WINDOW_HEIGHT+20))
        bg.setFill("black")
        bg.setOutline("black")
        bg.draw(window)
        self._current = []
        # here, you want to draw the tiles that are visible
        # and possible record them for future manipulation
        # you'll probably want to change this at some point to
        # get scrolling to work right...
        self.init_move(cy,  cx)

    def move(self, dx, dy, cx, cy):
        vX = VIEWPORT_WIDTH-1
        vY = VIEWPORT_HEIGHT-1
        for tile in self._current:
            tile.move(-dx*TILE_SIZE,-dy*TILE_SIZE)
            if tile.p1.x < 0 and tile.p1.x/TILE_SIZE +1 > VIEWPORT_WIDTH and tile.p1.y < 0 and title.p1.y/TILE_SIZE + 1 > VIEWPORT_HEIGHT:
                tile.undraw()
                self._current.remove(tile)


    def find_colors(self, x,y, elt):
        if self.tile(x,y) == 0:
            elt.setFill('lightgreen')
            elt.setOutline('lightgreen')
        if self.tile(x,y) == 1:
            elt.setFill('green')
            elt.setOutline('green')
        elif self.tile(x,y) == 2:
            elt.setFill('sienna')
            elt.setOutline('sienna')


    def init_move(self, cy, cx):
        for tile in self._current:
            tile.undraw()
        dx = (VIEWPORT_WIDTH-1)/2
        dy = (VIEWPORT_HEIGHT-1)/2
        for y in range(LEVEL_HEIGHT):
            for x in range(LEVEL_WIDTH):
                sx = (x-(cx-dx)) * TILE_SIZE
                sy = (y-(cy-dy)) * TILE_SIZE
                elt = Rectangle(Point(sx,sy),
                                Point(sx+TILE_SIZE,sy+TILE_SIZE))
                self._current.append(elt)
                self.find_colors(x,y, elt)
                elt.draw(self._window)
        self.move(0,0, cx, cy)


    # return the tile at a given tile position
    def tile (self,x,y):
        return self._level.tile(x,y)

    # add a thing to the screen at a given position
    def add (self,item,x,y):
        # first, move object into given position
        item.sprite().move((x-(self._cx-(VIEWPORT_WIDTH-1)/2))*TILE_SIZE,
                           (y-(self._cy-(VIEWPORT_HEIGHT-1)/2))*TILE_SIZE)
        item.sprite().draw(self._window)
        # WRITE ME!   You'll have to figure out how to manage these
        # because chances are when you scroll these will not move!


    # helper method to get at underlying window
    def window (self):
        return self._window


