#############################################################
# 
# A function that expands on Character functionality
# An NPC has knowledge that he or she can share with the player
# The NPC can also sell to the player and heal him or her for a price




from character import *
import time
from screen import *
import random

class NPC (Character):
    def __init__ (self,name,desc, health, knowledge, items):
        Character.__init__(self,name,desc, health, items)

        pic = random.choice(['npc1.gif', 'npc2.gif', 'npc3.gif'])
        self._sprite = Image(Point(TILE_SIZE/2,TILE_SIZE/2),pic)

        self._direction = random.randrange(4)
        self._knowledge = knowledge

# Once the player has selected an item that he or she would like to buy,
# this function removes gold from the player, adds the item to his or her inventory,
    def sold(self,item, player):
        self._items.remove(item)
        player.changeGold(-item._price)
        player.addInventory(item)
        self._screen._dButtons.remove(item)
       
# the talk function calls screen to display any knowledge the NPC has in a dialogue box 
    def talk(self):
        self._screen.makeDialogue("talk", self._name, self._knowledge, self._items)

# the sell function calls screen to display any items the NPC has to sell
    def sell(self):
        self._screen.makeDialogue("sell", self._name, self._knowledge, self._items)

# the heal function calls screen to indicate to the player that he is being healed and that it costs gold
    def heal(self):
        self._screen.makeDialogue("heal", self._name, self._knowledge, self._items)

