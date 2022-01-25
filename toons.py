from math import pi, sin, cos
from turtle import speed
from direct.showbase.Messenger import Messenger
from panda3d.core import CollisionCapsule, CollisionNode, BitMask32
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
        super().__init__(base, 3, pos, Hpr, 1, cname="ToonColider")
    
    

class state():
    startaction = None # the command to start with
    endaction = None # The command to end with
    durration = -1 #The durration it should end with
    def __init__(self, start, end):
        self.startaction = start
        self.endaction = end
    
    def start(self, prevstate = None):
        if prevstate is not None:
            prevstate.endaction()
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
    movestate = 0
    istugging = False
    speed_cont = 20
    tug_offsetX = pi/2
    tug_offsetY = 0
    tug_orgin = Point3(0,0,0)
    tug_prev = 0
    speed_tug = 5
    def __init__(self, base, pos, Hpr):
        super().__init__(base, pos, Hpr)
        self.linecolider = CollisionCapsule(pos.getX(),pos.getY(),pos.getZ(),0,-10,3,0.5)
        self.linenode = self.avatar.attachNewNode(CollisionNode("TapeCollider"))
        #self.linenode.node().set_into_collide_mask(1)
        self.linenode.node().setFromCollideMask(BitMask32.bit(0))
        self.linenode.node().setIntoCollideMask(BitMask32.allOff())
        self.linenode.node().addSolid(self.linecolider)
        self.linenode.show()
        
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
    
    def canTug(self, tug):
        if (tug == 2):
            self.tug_orgin = self.getPos()
        else:
            self.tug_offsetX = pi/2
            self.tug_offsetY = 0
        self.movestate = tug
        
    def update_tug(self):
        print(self.getHpr())

    def update_move(self):
        deltax = 0
        deltay = 0
        rotation = 0
        didrot = False
        zcalc = True
        dt = globalClock.getDt()
        #print(self.movestate)
        if self.movement_dict["interact"]:
            self.movement_dict["interact"] = False
            messenger.send("Interacting")
        if self.movestate == 1:#Handles movement around the level
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

        elif self.movestate == 2:#Handles tugging stuff
            #Funcitons of movement
            #Degree of Left and Right X = cos(f)
            #Degree of Tugging Back Y = -(sin(f) + t) + 1
            #f = tugging ammount left (-) and right (+), 0 <= x <= pi
            #t = elaped time 
            #Then for tugging location just use Actor1.lookAt(Actor2)
            if self.movement_dict["left"]:
                if (self.tug_offsetX > 0):
                    self.tug_offsetX = self.tug_offsetX - 0.1  * 25 * dt
                if (self.tug_prev != -0.1):
                    self.tug_offsetY = self.tug_offsetY + 1  * 5 * dt
                    self.tug_prev = -0.1
            elif self.movement_dict["right"]:
                if (self.tug_offsetX < pi):
                    self.tug_offsetX = self.tug_offsetX + 0.1  * 25 * dt
                if (self.tug_prev != 0.1):
                    self.tug_offsetY = self.tug_offsetY + 1  * 15 * dt
                    self.tug_prev = 0.1
            newpos = self.tug_orgin + Point3(-cos(self.tug_offsetX)*self.tug_offsetY,-(sin(self.tug_offsetX)*self.tug_offsetY) + 1,0)
            self.setPos(newpos)
            




        
        
    def walk(self, bol):
        if (bol and (self.ismoving == False)):
            self.avatar.loop("walk")
        elif ((bol == False) and (self.ismoving == True)):
            self.avatar.stop()
