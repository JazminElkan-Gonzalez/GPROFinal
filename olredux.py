from util import *
from level import *
from screen import *
from queue import *
from status import *
from rat import *
from player import *
from cinput import *
from zombie import *
from npc import *
from feather import *
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
                      WINDOW_WIDTH+WINDOW_RIGHTPANEL, WINDOW_HEIGHT+WINDOW_LEFTPANEL,
                      autoflush=False)

    level = Level()
    log ("level created")
    playerX = LEVEL_WIDTH-18
    playerY = 11
    scr = Screen(level,window,playerX ,playerY)
    log ("screen created")

    q = EventQueue()

    OlinStatue("Olin statue","A statue of F. W. Olin", 5000).materialize(scr,20,20)

    # Rat("Brain","A rat with a big head").register(q,600).materialize(scr,10,30)
    Rat("Pinky","A rat", 50).register(q,400).materialize(scr,30,30)
    Feather("FeatheryFeather", "A fluffy feather. I bet Zombies like it!", 10).materialize(scr,LEVEL_WIDTH-5,15)
    #Town Folk
    fluf = Feather("Feathery", "A fluffy feather. I bet Zombies like it!", 10)
    NPC("Bub","Blacksmith", 5, "It's so hard to make a living these days...", [fluf]).register(q,400).materialize(scr,LEVEL_WIDTH-20,7)
    NPC("Sarah","Child", 5, "Mommy and Daddy went south... but they have not come back... :(", []).register(q,400).materialize(scr,LEVEL_WIDTH-26,7)
    NPC("Carter","Warrior", 5, "Lotta folks gon missin out west", []).register(q,400).materialize(scr,LEVEL_WIDTH-25,13)
    NPC("Gregory","Grizzled Old Man", 5, "Stay away from gravestones with large decayed areas around them", []).register(q,400).materialize(scr,LEVEL_WIDTH-21,13)
    NPC("Anthony","Servant of The Court", 5, "Beware! The king has been behaving strangely...", []).register(q,400).materialize(scr,LEVEL_WIDTH-17,11)
    Zombie("ZOMZOM", "ZOOM ZOOM", 50).register(q,100).materialize(scr,28,23)
    Zombie("brains", "A ZOMBIE WHO LIKES BRAINSSSSS", 50).register(q,100).materialize(scr,28,22)
    flaf = Feather("Feather", "A fluffy feather. I bet Zombies like it!", 10)

    create_panel(window)

    p = Player(30, "...what's your name, bub?...", [flaf], 10).materialize(scr,playerX ,playerY)

    q.enqueue(1,CheckInput(window,p))
    q.enqueue(1,scr)

    while True:
        # Grab the next event from the queue if it's ready
        q.dequeue_if_ready()
        # Time unit = 10 milliseconds
        time.sleep(0.01)



if __name__ == '__main__':
    main()
