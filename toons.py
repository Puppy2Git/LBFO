from types import new_class
from props import propos
from panda3d.core import Point3
import sys

class toon(propos):
    '''
    This class in a subclass of the propos class\n
    It allows for the creation of the toon characters
    which will be used by the player or by the server.\n
    This will not be called for normaly and is meant for\n
    subclasses
    '''
    def __init__(self, base, pos):
        super().__init__(base, 0, pos)



class controllerToon(toon):
    movement_dict = {"left": False, 
    "right" : False,
    "up" : False,
    "down" : False,
    "interact" : False}
    speed_cont = 15
    def __init__(self, base, pos):
        super().__init__(base, pos)
        
        #Creating keyboard events for the ShowBase for movement
        base.accept("escape",sys.exit)
        #Up
        base.accept("arrow_up", self.setKey, ["up", True])
        base.accept("arrow_up-up", self.setKey, ["up", False])
        #Down
        base.accept("arrow_down", self.setKey, ["down", True])
        base.accept("arrow_down-up", self.setKey, ["down", False])
        #Left
        base.accept("arrow_left", self.setKey, ["left", True])
        base.accept("arrow_left-up", self.setKey, ["left", False])
        #Right
        base.accept("arrow_right", self.setKey, ["right", True])
        base.accept("arrow_right-up", self.setKey, ["right", False])
        
        base.accept("space", self.setKey, ["interact" , True])

    def setKey(self, key, val):
        self.movement_dict[key] = val
        
    
    def update_move(self, task):
        deltax = 0
        deltay = 0
        if globalClock != None:
            dt = globalClock.getDt()

        if self.movement_dict["left"] and not self.movement_dict["right"]:
            deltax = -self.speed_cont
        elif self.movement_dict["right"] and not self.movement_dict["left"]:
            deltax = self.speed_cont
        if self.movement_dict["up"] and not self.movement_dict["down"]:
            deltay = self.speed_cont
        elif self.movement_dict["down"] and not self.movement_dict["up"]:
            deltay = -self.speed_cont
        newpos = self.getPos() + Point3(deltax * dt,deltay * dt,0)
        self.setPos(newpos)
        return task.cont
