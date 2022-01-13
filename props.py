from direct.actor.Actor import Actor
from direct.showbase.DirectObject import DirectObject
import panda3d
from panda3d.core import CollisionSphere
from panda3d.core import CollisionNode
from panda3d.core import CollisionCapsule

from panda3d.core import Point3
class props_dicts:
    #Model location, model animation locations,collision offset, collision radius
    models = [ [["models/panda",{"walk":"models/panda-walk"}] , CollisionSphere(0,0,6,6)] ,
    [["models/panda",{"walk":"models/panda-walk"}],CollisionSphere(0,0,10,10)],
    [["models/LB_bookshelf"],CollisionCapsule(-4,0,1, 4,0,1, 1)]]

class propos(DirectObject):
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
            print("Made actor")
        else:
            self.avatar = self.base.loader.loadModel(props_dicts.models[modelN][0][0])#Otherwise if they are a prop
            print("Made Prop")
        self.avatar.reparentTo(base.render) # Set avatar tied to game
        self.avatar.setPos(pos)#Setting the position of the Actor
        self.avatar.setHpr(hpr)
        self.avatar.setScale(scale)
        self.nodePath = self.avatar.attachNewNode(CollisionNode("cnode"))#New collision Node
        self.collider = props_dicts.models[modelN][1] # create colision sphere
        self.nodePath.node().addSolid(self.collider) # Adding collider to avatar
        
    
    def debug_showcolision(self):
        self.nodePath.show()

    def setPos(self,pos=Point3(0,0,0)):
        self.avatar.setPos(pos)

    def fluidMove(self,pos = Point3(0,0,0)):
        self.avatar.posInterval(1, Point3(20, 0, 0), startPos=Point3(-20, 0, 0), fluid=1).loop()
    def getPos(self):
        return self.avatar.getPos()
    
    def setHpr(self,Hpr):
        self.avatar.setHpr(Hpr)
    def getHpr(self):
        return self.avatar.getHpr()
