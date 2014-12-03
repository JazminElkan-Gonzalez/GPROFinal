from util import *
from level import *
from screen import *
from queue import *
from status import *
from rat import *
from player import *
from cinput import *
from zombie import *
############################################################
#
# Olinland Redux
#
# Scaffolding to the final project for Game Programming
#
#


#
# The main function
# 
# It initializes everything that needs to be initialized
# Order is important for graphics to display correctly
# Note that autoflush=False, so we need to explicitly
# call window.update() to refresh the window when we make
# changes
#
def main ():

    window = GraphWin("Olinland Redux", 
                      WINDOW_WIDTH+WINDOW_RIGHTPANEL, WINDOW_HEIGHT,
                      autoflush=False)

    level = Level()
    log ("level created")

    scr = Screen(level,window,25,25)
    log ("screen created")

    q = EventQueue()

    OlinStatue("Olin statue","A statue of F. W. Olin", 5000).materialize(scr,20,20)

    # Rat("Brain","A rat with a big head").register(q,600).materialize(scr,10,30)
    Rat("Pinky","A rat", 50).register(q,400).materialize(scr,30,30)

    Zombie("ZOMZOM", "ZOOM ZOOM", 50).register(q,250).materialize(scr,27,23)

    create_panel(window)

    p = Player(30, "...what's your name, bub?...").materialize(scr,25,25)

    q.enqueue(1,CheckInput(window,p))
    q.enqueue(1,scr)

    while True:
        # Grab the next event from the queue if it's ready
        q.dequeue_if_ready()
        # Time unit = 10 milliseconds
        time.sleep(0.01)



if __name__ == '__main__':
    main()
