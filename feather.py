#############################################################
# 
# A function that expands on Thing functionality
# A feather allows the player to add health to his or her zombies
# Feathers die once they have been used too many times. 
# In addition to what Things have, Feathers also have a user and a price. 




from thing import *




class Feather  (Thing):
    def __init__ (self,name,desc, health):
        Thing.__init__(self,name,desc, health)
        self._pic = 'feather.gif'
        self._sprite = Image(Point(TILE_SIZE/2,TILE_SIZE/2),self._pic)

        self._user = None
        self._price = 10

# Removes health from the feather every time it is used
    def use(self):
        self._health = self._health - 1
        if self._health <= 0:
            self.die()

# Sets the current "user" or owner of the item when it is
# Added to the users inventory
    def pickup(self, user):
        self._user = user

# Destroys the Feather when it is out of uses, or zombies killed it
    def die(self):
        if self._user != None:
            self._user._inventory.remove(self)
        else:
            OBJECTS.remove(self)
            self._sprite.undraw()

# Check function to indicate what this "thing" is. This allows us to check the "type" of an object
# without having to us isinstance() 
    def is_character (self):
        return False

# Check function that allows other characters to know if they can walk over this Character
    def is_walkable (self):
        return True
