from direct.actor.Actor import Actor
from direct.showbase.DirectObject import DirectObject
import panda3d
from math import pi
from panda3d.core import CollisionSphere
from panda3d.core import CollisionNode
from panda3d.core import CollisionCapsule

from panda3d.core import Point3
class props_dicts:
    #Model location, model animation locations,collision offset, collision radius
    models = [ [["models/panda",{"walk":"models/panda-walk"}] , CollisionSphere(0,0,6,6)] ,
    [["models/panda",{"walk":"models/panda-walk"}],CollisionSphere(0,0,10,10)],
    [["models/LB_bookshelf"],CollisionCapsule(-4,0,1, 4,0,1, 1)]]

    directions = {
    'E' : 90.0,
    'W' : 270.0,
    'S' : 0.0,
    'N' : 180.0
    }

def getdir(di):
        return Point3(props_dicts.directions[di],0,0)

class propos(DirectObject):
    '''
    Props, are to be inherated by the toon, cog, stacks, memos or used as decoration\n
    You can create a prop using the following syntax\n
    base = ShowBase, modleN = The index of the model dict, pos = the Point 3 position, hpr = Point3 rotation, scale = scale of object\n
    >>>my_panda = propos(base, 0, Point3(0,0,0), Point3(0,0,0), 1)\n
    That will spawn a panda model at 0,0,0 with no rotation and a scale of 1
    '''
    avatar = None
    base = None
    collider = None
    nodePath = None

    def __init__(self, base, modelN = 0, pos = Point3(0,0,0), hpr = Point3(0,0,0), scale = 1):
        super().__init__()
        self.position = pos# Set position of class
        self.base = base # To get Base
        if len(props_dicts.models[modelN][0]) >= 2:#If has animations and is an actor
            self.avatar = Actor(props_dicts.models[modelN][0][0],props_dicts.models[modelN][0][1]) #New Avatar
        else:
            self.avatar = self.base.loader.loadModel(props_dicts.models[modelN][0][0])#Otherwise if they are a prop
        self.avatar.reparentTo(base.render) # Set avatar tied to game
        self.avatar.setPos(pos)#Setting the position of the Actor
        self.avatar.setHpr(hpr)
        self.avatar.setScale(scale)
        self.nodePath = self.avatar.attachNewNode(CollisionNode("cnode"))#New collision Node
        self.collider = props_dicts.models[modelN][1] # create colision sphere
        self.nodePath.node().addSolid(self.collider) # Adding collider to avatar
        
    
    def debug_showcolision(self):
        '''
        This is primarly used for debug, wether it is to print information and show collision\n
        This should only be refrenced in the GameLogic class
        '''
        self.nodePath.show()

    def setPos(self,pos=Point3(0,0,0)):
        '''
        Used to set posiiton of the actor\n
        pos = posiiton as a Point3\n
        >>>my_prop.setPos(Point3(0,10,0))\n
        sets my_prop position to 0,10,0
        '''
        self.avatar.setPos(pos)

    def getPos(self):
        '''
        Used to return the position of the actor\n
        Takes no arguments\n
        >>>my_prop.getPos()\n
        returns the actor position as a Point3
        '''
        return self.avatar.getPos()
    
    def setHpr(self,Hpr):
        
        self.avatar.setHpr(Hpr)
    def getHpr(self):
        return self.avatar.getHpr()
