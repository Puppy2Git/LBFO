from direct.actor.Actor import Actor
from direct.showbase.DirectObject import DirectObject
import panda3d
from panda3d.core import CollisionSphere
from panda3d.core import CollisionNode
from panda3d.core import Point3
class props_dicts:
    #Model location, model animation locations,collision offset, collision radius
    models = [["models/panda",{"walk":"models/panda-walk"},6,6]]

class propos(DirectObject):
    position = []
    avatar = None
    base = None
    collider = None
    def __init__(self, base, modelN = 0, pos = [0,0,0]):
        super().__init__()
        self.position = pos# Set position of class
        self.base = base # To get Base
        self.avatar = Actor(props_dicts.models[modelN][0],props_dicts.models[modelN][1]) #New Avatar
        self.avatar.reparentTo(base.render) # Set avatar tied to game
        self.avatar.setPos(pos[0],pos[1],pos[2])#Setting the position of the Actor
        self.nodePath = self.avatar.attachNewNode(CollisionNode("cnode"))#New collision Node
        self.collider = CollisionSphere(0,0,props_dicts.models[modelN][2], props_dicts.models[modelN][3]) # create colision sphere
        self.nodePath.node().addSolid(self.collider) # Adding collider to avatar
        self.nodePath.show()


    def setPos(self,pos=[0,0,0],change=False):
        if not change:
            self.position = pos
        else:
            self.position += pos
        self.avatar.setPos(pos[0],pos[1],pos[2])
        

    def fluidMove(self):
        self.avatar.posInterval(5, Point3(20, 0, 0), startPos=Point3(-20, 0, 0), fluid=1).loop()
    def getPos(self):
        return self.position
