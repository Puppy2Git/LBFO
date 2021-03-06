
from direct.actor.Actor import Actor
from direct.showbase.DirectObject import DirectObject
from direct.showbase.Loader import Loader
import panda3d
from math import pi
from panda3d.core import CollisionSphere, CollisionNode, CollisionCapsule, BitMask32, Point3


class props_dicts:
    #Model location, model animation locations,collision offset, collision radius
    models = [[["models/panda",{"walk":"models/panda-walk"}], CollisionSphere(0,0,3,3)] ,#Default Actor
    [["models/panda",{"walk":"models/panda-walk"}],CollisionCapsule(-1,0,1, 1,0,1, 1)],#Full Wall
    ["models/LB_bookshelf","**/collision"],#Bookshelf
    [["models/toon", None], CollisionSphere(0,0,3,3)],
    ["models/level", None]#Toon Model
    ]

    directions = {
    'E' : 90.0,
    'W' : 270.0,
    'S' : 0.0,
    'N' : 180.0
    }

def getdir(di):
        return Point3(props_dicts.directions[di],0,0)

props = []

proplocations = [[2,Point3(10,10,0),getdir('S'),1],
[2,Point3(-20,10,0),getdir('S'),1]
]


class propos(DirectObject):
    '''
    Props, are to be inherated by the toon, cog, stacks, memos or used as decoration\n
    You can create a prop using the following syntax\n
    Don't simply strech models to use as a scene, create that stuff in blender!
    base = ShowBase, modleN = The index of the model dict, pos = the Point 3 position, hpr = Point3 rotation, scale = scale of object\n
    >>> my_panda = propos(base, 0, Point3(0,0,0), Point3(0,0,0), 1)\n
    That will spawn a panda model at 0,0,0 with no rotation and a scale of 1
    '''
    avatar = None
    base = None
    collider = None
    nodePath = None

    def __init__(self, base, modelN = 0, pos = Point3(0,0,0), hpr = Point3(0,0,0), scale = Point3(1,1,1), cname = "cnode", isactor = False, issuper = False):
        global props
        super().__init__()#Inits as a direct object
        self.position = pos# Set position of class
        self.base = base # To get Base
        #self.avatar = props_dicts.models[modelN][0]#The model from the model Number
        
        
        if (isactor):#If it is an actor
            self.avatar = Actor(props_dicts.models[modelN][0][0],props_dicts.models[modelN][0][1])
            self.avatar.reparentTo(base.render) # Set avatar tied to game
            self.nodePath = self.avatar.attachNewNode(CollisionNode(cname))#New collision Node
            self.collider = props_dicts.models[modelN][1] # create colision sphere
            self.nodePath.node().addSolid(self.collider) # Adding collider to avatar
            
        else:#Otherwise it is a model
            self.avatar = self.base.loader.loadModel(props_dicts.models[modelN][0])#Set the model
            self.avatar.reparentTo(base.render) # Set avatar tied to game
            if (len(props_dicts.models[modelN]) == 2):#Model collision
                if(props_dicts.models[modelN][1] is not None):
                    self.collider = self.avatar.find(props_dicts.models[modelN][1])#Collider
                    self.collider.node().setIntoCollideMask(BitMask32.bit(0))#Bitmask to collide with all
        self.avatar.setPos(pos)#Setting the position of the Actor
        self.avatar.setHpr(hpr)#Set rotation
        self.avatar.setScale(scale)#Set scale
        if (not issuper):
            self.modelID = len(props)
            props.append(self)
    def destroy(self):
        '''
        Called when the actor is time to go bye bye\n
        >>> my_prop.destroy()\n
        that's it
        '''

        self.avatar.delete()


    def debug_showcolision(self):
        '''
        This is primarly used for debug, wether it is to print information and show collision\n
        This should only be refrenced in the GameLogic class\n
        >>> my_prop.debug_showcolision()
        '''
        if (self.nodePath is not None):
            self.nodePath.show()
        elif (self.collider is not None):
            self.collider.show()
        
            

    def setPos(self,pos=Point3(0,0,0)):
        '''
        Used to set posiiton of the actor\n
        pos = posiiton as a Point3\n
        >>> my_prop.setPos(Point3(0,10,0))\n
        sets my_prop position to 0,10,0
        '''
        self.avatar.setPos(pos)

    def getPos(self):
        '''
        Used to return the position of the actor\n
        Takes no arguments\n
        >>> my_prop.getPos()\n
        returns the actor position as a Point3
        '''
        return self.avatar.getPos()
    
    def setHpr(self,Hpr):
        '''
        Used to set the rotation of the actor\n
        Takes a Point3 object\n
        >>> my_prop.setHpr(Point3(0,0,0))\n
        sets the actor position to 0,0,0
        '''
        self.avatar.setHpr(Hpr)

    def getHpr(self):
        '''
        Used to get the rotation of the actor\n
        Takes no arguments\n
        >>> my_prop.getHpr()\n
        returns the action position as a Point3
        '''
        return self.avatar.getHpr()


def debug_showcolision():
    global props
    for poo in props:
        poo.debug_showcolision()