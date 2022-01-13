from direct.showbase.DirectObject import DirectObject
import ohmyears
from props import propos
from ohmyears import soundManager
import toons
from panda3d.core import Point3
from math import pi
class gameWorld(DirectObject):
    tugging = False
    def __init__(self, base):
        self.base = base
        super().__init__()
        self.sound = soundManager(self.base)
        self.accept('Interacting',self.interacting)


    
    def initWorld(self):
        self.mainchar = toons.controllerToon(self.base, Point3(20,20,0),Point3(0,0,0),1)
        self.bookshelf = propos(self.base,2,Point3(-20,0,0),Point3((1 * 180) / (180 * pi),0,0),2)
        
        self.mainchar.debug_showcolision()
        self.bookshelf.debug_showcolision()

    def interacting(self):
        self.tugging = not self.tugging
        self.sound.ToggleMusic()

    def toon_updateloop(self, task):
        self.mainchar.update_move()#Updates player movement
        return task.cont