#Important Panda3D Imports
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from panda3d.core import CollisionTraverser, CollisionHandlerPusher
from panda3d.core import Point3
from math import pi
#Custom Imports
import elevators
import cogs
import obstacles
from props import propos
import toons
from ohmyears import soundManager
from gameLogic import gameWorld
debug = False
class AppGame(ShowBase):
    targetObj = None
    def __init__(self):
        super().__init__(self)#Inits the ShowBase
        self.gameworld = gameWorld(self,debug)#Creates the gameworld
        self.gameworld.initWorld()#Initalizes the gameworld
        self.cTrav = CollisionTraverser()#Added the Collision Traverser
        self.pusherh = CollisionHandlerPusher()#Adds a Collision Hanlder for Pushing
        self.pusherh.setHorizontal(True)

        #Camera will be weird otherwise without disabling mouse
        self.disable_mouse()
        self.camera.setHpr(0,pi * 90,0)

        #Note: may need to add back: ,self.drive.node()
        self.cTrav.addCollider(self.gameworld.mainchar.nodePath, self.pusherh)#Adds Collider NotePath and Collision Handler to traverser
        self.pusherh.addCollider(self.gameworld.mainchar.nodePath, self.gameworld.mainchar.avatar)#Adds NodePath, Avatar, and base note of the collider
        
        
        
        self.targetObj = self.gameworld.mainchar#Sets the target for the camera
        self.taskMgr.add(self.gameworld.toon_updateloop, "movement_update")#So the toons update
        self.taskMgr.add(self.followObject, "camera_update")#So the camera can update
        self.taskMgr.add(self.gameworld.sound.update_musicshift, "music_update")#So that the music can change

    def followObject(self, task):
        lookpos = self.targetObj.getPos() + Point3(0,-30,175)
        
        self.camera.setPos(lookpos)
        
        return task.cont


game = AppGame()
game.run()
