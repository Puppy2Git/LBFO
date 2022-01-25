#Important Panda3D Imports
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from panda3d.core import CollisionTraverser, CollisionHandlerPusher, CollisionHandlerEvent
from panda3d.core import Point3
from panda3d.core import NodePath
from math import pi
from panda3d.core import loadPrcFileData
loadPrcFileData("", "want-directtools #t")
loadPrcFileData("", "want-tk #t")
#Custom Imports

from gameLogic import gameWorld
debug = True
class AppGame(ShowBase):
    targetObj = None
    def __init__(self):
        super().__init__(self)#Inits the ShowBase
        self.gameworld = gameWorld(self,debug)#Creates the gameworld
        self.gameworld.initWorld()#Initalizes the gameworld
        self.cTrav = CollisionTraverser()#Added the Collision Traverser
        self.pusherh = CollisionHandlerPusher()#Adds a Collision Hanlder for Pushing
        self.eventh = CollisionHandlerEvent()
        self.eventh.addInPattern('%fn')
        self.pusherh.setHorizontal(True)

        #Camera will be weird otherwise without disabling mouse
        self.disable_mouse()
        self.camera.setHpr(0,275,0)

        #Note: may need to add back: ,self.drive.node()
        self.cTrav.addCollider(self.gameworld.mainchar.nodePath, self.pusherh)#Adds Collider NotePath and Collision Handler to traverser
        self.cTrav.addCollider(self.gameworld.mainchar.linenode, self.eventh)
        #print(self.gameworld.bookshelf1.collider.ls())
        self.cTrav.addCollider(self.gameworld.stack.nodePath, self.eventh)
        self.pusherh.addCollider(self.gameworld.mainchar.nodePath, self.gameworld.mainchar.avatar)#Adds NodePath, Avatar, and base note of the collider
        
        
        
        self.targetObj = self.gameworld.mainchar#Sets the target for the camera
        self.taskMgr.add(self.gameworld.toon_updateloop, "movement_update")#So the toons update
        self.taskMgr.add(self.followObject, "camera_update")#So the camera can update
        self.taskMgr.add(self.gameworld.sound.update_musicshift, "music_update")#So that the music can change

    def followObject(self, task):
        lookpos = self.targetObj.getPos() + Point3(0,-10,70)
        
        self.camera.setPos(lookpos)
        
        return task.cont


game = AppGame()

game.run()
