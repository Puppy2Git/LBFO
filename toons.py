from math import pi
from direct.showbase.Messenger import Messenger
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
    def __init__(self, base, pos, Hpr):
        super().__init__(base, 3, pos, Hpr, 1)
    
    

class state():
    startaction = None # the command to start with
    endaction = None # The command to end with
    durration = -1 #The durration it should end with
    def __init__(self, start, end, durration):
        self.startaction = start
        self.endaction = end
        self.durration = durration
    
    def start(self, prevstate = None):
        if prevstate is not None:
            prevstate.end()
        self.startaction()

    def end(self):
        self.endaction()

class controllerToon(toon):
    movement_dict = {"left": False, 
    "right" : False,
    "up" : False,
    "down" : False,
    "interact" : False}
    ismoving = False
<<<<<<< Updated upstream
    speed_cont = 20
    def __init__(self, base, pos, Hpr):
        super().__init__(base, pos, Hpr)
=======
    movestate = False
    speed_cont = 25
    def __init__(self, base, pos, Hpr, scale):
        super().__init__(base, pos, Hpr,scale)
>>>>>>> Stashed changes
        self.avatar.setPlayRate(2, "walk")
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
        
    def canMove(self, move):
        self.movestate = move

    def update_move(self):
        deltax = 0
        deltay = 0
        rotation = 0
        didrot = False
        zcalc = True
        dt = globalClock.getDt()
        if self.movement_dict["interact"]:
            self.movement_dict["interact"] = False
            messenger.send("Interacting")
        if self.movestate:
            if self.movement_dict["left"] and not self.movement_dict["right"]:
                rotation = rotation - 90
                deltax = -self.speed_cont
                zcalc = False
                didrot = True
            elif self.movement_dict["right"] and not self.movement_dict["left"]:
                rotation = rotation + 90
                deltax = self.speed_cont
                zcalc = False
                didrot = True
            if self.movement_dict["up"] and not self.movement_dict["down"]:
                if (zcalc):
                    rotation = 180
                else:
                    if (rotation <= 0):
                        rotation = rotation - 45
                    else:
                        rotation = rotation + 45
                didrot = True
                deltay = self.speed_cont
            elif self.movement_dict["down"] and not self.movement_dict["up"]:
                if (zcalc):
                    rotation = 0
                else:
                    if (rotation >= 0):
                        rotation = rotation - 45
                    else:
                        rotation = rotation + 45
                didrot = True
                deltay = -self.speed_cont
            
        if (didrot):
            self.setHpr(Point3(rotation,0,0))
        self.walk(((deltax != 0) or (deltay != 0)))
        self.ismoving = ((deltax != 0) or (deltay != 0))

        newpos = self.getPos() + Point3(deltax * dt,deltay * dt,0)
        self.setPos(newpos)
        
    def walk(self, bol):
        if (bol and (self.ismoving == False)):
            self.avatar.loop("walk")
        elif ((bol == False) and (self.ismoving == True)):
            self.avatar.stop()
