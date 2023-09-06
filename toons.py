from math import pi, sin, cos
from turtle import speed
from direct.showbase.Messenger import Messenger
from panda3d.core import CollisionCapsule, CollisionNode, BitMask32, Point3
from props import propos

import sys
toons = []

class toon(propos):
    '''
    This class in a subclass of the propos class\n
    It allows for the creation of the toon characters
    which will be used by the player or by the server.\n
    This will not be called for normaly and is meant for\n
    subclasses
    '''
    def __init__(self, base, pos, Hpr):
        global toons
        super().__init__(base, 3, pos, Hpr, 1, cname="ToonColider", isactor=True, issuper=True)
        self.toonID = len(toons)
        toons.append(self)
    
    

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
    stack_to_look_at = None
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
        self.linecolider = CollisionCapsule(pos.getX(),pos.getY(),pos.getZ(),0,5,3,0.5)
        self.linenode = self.avatar.attachNewNode(CollisionNode("FanCollider"))
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
        '''
        Called by keyboard event\n
        Used to set the key state given the key\n
        Called only by base.accept()\n
        >>> base.accept("key", self.setKey, ["right", True])\n
        Sets the right movement to truea
        '''
        self.movement_dict[key] = val
        
    def canMove(self, move):
        '''
        Sets the movement state of the controller\n
        0 = no movement\n
        1 = Normal Movement\n
        2 = Tugging Movement\n
        Called by outside souces\n
        >>> my_toon.canMove(0)\n
        The toon cannot move now
        '''
        self.movestate = move
    
    #To be obsolete
    def canTug(self, tug, looking):
        '''
        Sets the state of if it can Tug\n
        Takes in the tug state and the target stack\n
        >>> my_toon.canTug(2, stack)\n
        It will begin to tug with a target stack
        '''
        self.stack_to_look_at = looking
        if (tug == 2):
            self.tug_orgin = self.stack_to_look_at.getParent().getPos()#Sets the position
            self.tug_offsetY = 3 #Distance of radius of stack
        else:
            self.tug_offsetX = pi/2
            self.tug_offsetY = 0
        self.movestate = tug
        

    def update_move(self):
        '''
        Major Movement Function\n
        Only Should be called in main update loop\n
        '''
        deltax = 0
        deltay = 0
        dt = globalClock.getDt()
        
        if self.movement_dict["interact"]:#Interact
            self.movement_dict["interact"] = False
            messenger.send("Interacting")
        if self.movestate == 1:#Handles movement around the level
            if self.movement_dict["left"] and not self.movement_dict["right"]:#Left
                deltax = -self.speed_cont
            elif self.movement_dict["right"] and not self.movement_dict["left"]:#Right
                deltax = self.speed_cont
            if self.movement_dict["up"] and not self.movement_dict["down"]:#Up
                deltay = self.speed_cont
            elif self.movement_dict["down"] and not self.movement_dict["up"]:#Down
                deltay = -self.speed_cont
            self.walk(((deltax != 0) or (deltay != 0)))
            self.ismoving = ((deltax != 0) or (deltay != 0))
            newpos = self.getPos() + Point3(deltax * dt,deltay * dt,0)
            if (self.ismoving):
                self.avatar.lookAt(newpos)
            self.setPos(newpos)        

        #Do be obsolete
        elif self.movestate == 2:#Handles tugging stuff
            #Funcitons of movement
            #Degree of Left and Right X = cos(f)*length
            #Degree of Tugging Back Y = -(sin(f) + t)*length
            #f = tugging ammount left (-) and right (+), 0 <= x <= pi
            #t = elaped time 
            #Then for tugging location just use Actor1.lookAt(Actor2)
            if (self.movement_dict["left"] and not self.movement_dict["right"]):#Left
                if (self.tug_offsetX > 0):#If it is not too far to the left
                    self.tug_offsetX = self.tug_offsetX - 0.1  * 25 * dt
                if (self.tug_prev != -0.1):
                    #self.tug_offsetY = self.tug_offsetY + 1  * 5 * dt
                    self.tug_prev = -0.1
                    messenger.send("Heave hoe")
            elif (self.movement_dict["right"] and not self.movement_dict["left"]):#Right
                if (self.tug_offsetX < pi):#If it is not too far to the right
                    self.tug_offsetX = self.tug_offsetX + 0.1  * 25 * dt
                if (self.tug_prev != 0.1):
                    #self.tug_offsetY = self.tug_offsetY + 1  * 15 * dt
                    self.tug_prev = 0.1
                    messenger.send("Heave hoe")
            #New Pos
            newpos = self.tug_orgin + Point3(-cos(self.tug_offsetX)*self.tug_offsetY,-(sin(self.tug_offsetX)*self.tug_offsetY),0)
            #move
            self.setPos(newpos)
            #New stack
            self.avatar.lookAt(self.stack_to_look_at)
            
            
    def walk(self, bol):
        '''
        Handles movement of animaiton\n
        called within the movement thing\n
        >>> self.walk(True)\n
        Loops the walking animation
        '''
        if (bol and (self.ismoving == False)):
            self.avatar.loop("walk")
        elif ((bol == False) and (self.ismoving == True)):
            self.avatar.stop()
