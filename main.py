#Important Panda3D Imports
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from panda3d.core import CollisionTraverser, CollisionHandlerPusher

#Custom Imports
import elevators
import cogs
import obstacles
from props import propos
import toons

class AppGame(ShowBase):
    def __init__(self):
        super().__init__()#Inits the ShowBase
        self.cTrav = CollisionTraverser()#Added the Collision Traverser
        self.pusherh = CollisionHandlerPusher()#Adds a Collision Hanlder for Pushing
        self.test = propos(self,0,[0,5,0])#Inits Obj 1
        self.test2 = propos(self,0,[0,0,0])#Inits Obj 2
        self.cTrav.addCollider(self.test2.nodePath, self.pusherh)#Adds Collider NotePath and Collision Handler to traverser
        
        #Note: may need to add back: ,self.drive.node()
        self.pusherh.addCollider(self.test2.nodePath, self.test2.avatar)#Adds NodePath, Avatar, and base note of the collider
        self.test2.fluidMove()#Move loops the character



game = AppGame()
game.run()
