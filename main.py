#Important Panda3D Imports
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from panda3d.core import CollisionTraverser, CollisionHandlerPusher
from panda3d.core import Point3
#Custom Imports
import elevators
import cogs
import obstacles
from props import propos
import toons
from ohmyears import soundManager

class AppGame(ShowBase):
    targetObj = None
    def __init__(self):
        super().__init__(self)#Inits the ShowBase
        self.cTrav = CollisionTraverser()#Added the Collision Traverser
        self.pusherh = CollisionHandlerPusher()#Adds a Collision Hanlder for Pushing
        self.test = propos(self,1,Point3(0,5,0))#Inits Obj 1
        self.test.debug_showcolision()
        self.mainchar = toons.controllerToon(self, Point3(20,20,0))
        self.targetObj = self.mainchar
        self.mainchar.debug_showcolision()
        self.pusherh.setHorizontal(True)
        #Camera will be weird otherwise without disabling mouse
        self.disable_mouse()
        self.camera.setHpr(0,-80,0)

        #Note: may need to add back: ,self.drive.node()
        self.cTrav.addCollider(self.mainchar.nodePath, self.pusherh)#Adds Collider NotePath and Collision Handler to traverser
        self.pusherh.addCollider(self.mainchar.nodePath, self.mainchar.avatar)#Adds NodePath, Avatar, and base note of the collider
        self.sound = soundManager(self)
        
        
        
        self.taskMgr.add(self.mainchar.update_move, "print_update")
        self.taskMgr.add(self.followObject, "camera_update")

    # def constant_print(self, task):
    #     if self.mainchar != None:
    #         print(self.mainchar.movement_dict)
    #     return Task.cont
    def followObject(self, task):
        lookpos = self.targetObj.getPos() + Point3(0,-10,100)
        
        self.camera.setPos(lookpos)
        return task.cont


game = AppGame()
game.run()
