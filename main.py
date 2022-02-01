#Important Panda3D Imports
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from panda3d.core import CollisionTraverser, CollisionHandlerPusher, CollisionHandlerEvent
from panda3d.core import Point3


#Debug stuff
#from panda3d.core import loadPrcFileData
#loadPrcFileData("", "want-directtools #t")
#loadPrcFileData("", "want-tk #t")
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
        self.eventh = CollisionHandlerEvent()#Adds a Collision Handler for events
        self.eventh.addInPattern('%fn-into-%in')#Adds an in pattern
        self.eventh.addOutPattern('%fn-exit-%in')#Adds an out pattern
        self.pusherh.setHorizontal(True)#Disables pushing on the Y-axis

        #Camera will be weird otherwise without disabling mouse
        self.disable_mouse()
        self.camera.setHpr(0,275,0)

        #Adds Collider NotePath and Collision Handler to traverser
        self.cTrav.addCollider(self.gameworld.mainchar.nodePath, self.pusherh)
        
        #Adds the Line Collider and the event
        self.cTrav.addCollider(self.gameworld.mainchar.linenode, self.eventh)
        
        #Adds the actor and the actor collider to the push handler
        self.pusherh.addCollider(self.gameworld.mainchar.nodePath, self.gameworld.mainchar.avatar)#Adds NodePath, Avatar, and base note of the collider
        
        self.targetObj = self.gameworld.mainchar#Sets the target for the camera
        self.taskMgr.add(self.gameworld.toon_updateloop, "movement_update")#So the toons update
        self.taskMgr.add(self.followObject, "camera_update")#So the camera can update
        self.taskMgr.add(self.gameworld.sound.update_musicshift, "music_update")#So that the music can change
        self.taskMgr.add(self.gameworld.tugging_updateloop, "tug_update")
    def followObject(self, task):
        '''
        This is used to follow the main character\n
        '''
        lookpos = self.targetObj.getPos() + Point3(0,-10,70)
        self.camera.setPos(lookpos)
        return task.cont


game = AppGame()

game.run()
