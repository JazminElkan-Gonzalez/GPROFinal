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
    playerX = LEVEL_WIDTH-34
    playerY = 11
    scr = Screen(level,window,playerX ,playerY)

    q = EventQueue()


    #Strat Area
    Zombie("ZOMZOM", "Your Only friend. Wake her up when you need her!! ", 50).register(q,28).materialize(scr,LEVEL_WIDTH-34,10)
    OlinStatue("King statue","King Prometheus once ruled these lands fairly. He was much loved", 5000).materialize(scr,LEVEL_WIDTH-35,10)
    
    #Zombies
    Zombie("Mommy", "A ZOMBIE WHO LIKES BRAINSSSSS", 10).register(q,50).materialize(scr,LEVEL_WIDTH-20,LEVEL_HEIGHT-30)
    Zombie("Daddy", "GIVE ME YOUR FACE", 50).register(q,50).materialize(scr,LEVEL_WIDTH-21,LEVEL_HEIGHT-30)
    zombieNames = ["Rhionnon", "Suellen", "Dewey", "Dortha", "Salvador", "Earlean", "Terence", "Earlean", "Terence", "Norman", "Chaya", "Cameron", "Sharee", "Blondell", "Charles", "Kori", "Florencia", "Gayle", "Lin", "Devona", "Trina", "Tessie"]
    for i in range(len(zombieNames)):
        x = random.randrange(1,LEVEL_WIDTH/2-10)
        y = random.randrange(1,LEVEL_HEIGHT-1)
        Zombie(zombieNames[i], "GGRRRRAAAAWWWWWW", (i+1)*10).register(q,50).materialize(scr,x,y)
    
    Zombie("King Prometheus the Green", "Your Biggest Mistake....", 2100).register(q,100).materialize(scr,LEVEL_WIDTH-10,10)

    #Castle
    Feather("FeatheryFeather", "A fluffy feather. I bet Zombies like it!", 10).materialize(scr,LEVEL_WIDTH-5,15)
    Rat("Brain","A rat with a big head", 50).register(q,600).materialize(scr,LEVEL_WIDTH-5,14)
    Rat("Pinky","A rat", 50).register(q,400).materialize(scr,LEVEL_WIDTH-6,15)
    
    #Town Folk
    fluf = Feather("Feathery", "A fluffy feather. I bet Zombies like it!", 10)
    flaf = Feather("Feather", "A fluffy feather. I bet Zombies like it!", 10)
    NPC("Bub","Blacksmith", 5, "It's so hard to make a living these days...", [fluf, flaf]).materialize(scr,LEVEL_WIDTH-20,7)
    NPC("Sarah","Child", 5, "Mommy and Daddy went south... but they have not come back... :(", []).materialize(scr,LEVEL_WIDTH-26,7)
    NPC("Carter","Warrior", 5, "Lotta folks gon missin out west", []).materialize(scr,LEVEL_WIDTH-25,13)
    NPC("Gregory","Grizzled Old Man", 5, "Stay away from gravestones with large decayed areas around them", []).materialize(scr,LEVEL_WIDTH-21,13)
    NPC("Anthony","Servant of The Court", 5, "Beware! The king has been behaving strangely...", []).materialize(scr,LEVEL_WIDTH-17,11)


    scr.init_move(playerY,  playerX)
    for item in OBJECTS:
        scr.add(item,item._x,item._y)

    create_panel(window)
    p = Player(30, "Life Mage", [], 10).materialize(scr,playerX ,playerY)



    q.enqueue(1,CheckInput(window,p))
    q.enqueue(1,scr)

    while True:
        # Grab the next event from the queue if it's ready
        q.dequeue_if_ready()
        # Time unit = 10 milliseconds
        time.sleep(0.01)



if __name__ == '__main__':
    main()
