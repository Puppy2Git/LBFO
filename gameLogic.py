from direct.showbase.DirectObject import DirectObject
import ohmyears
from props import propos
from ohmyears import soundManager
from props import getdir
import toons
from panda3d.core import Point3
from math import pi


class gameWorld(DirectObject):
    tugging = False
    debug = False
    def __init__(self, base, debug):
        self.base = base
        super().__init__()
        self.sound = soundManager(self.base)
        self.accept('Interacting',self.interacting)
        self.debug = debug


    
    def initWorld(self):
        self.mainchar = toons.controllerToon(self.base, Point3(20,20,0),getdir('S'))
        self.bookshelf1 = propos(self.base,2,Point3(-20,10,0),getdir('S'),1)
        self.bookshelf2 = propos(self.base,2,Point3(10,10,0),getdir('S'),1)
        self.level = propos(self.base,4,Point3(0,0,0))
        
        

        if (self.debug):
            self.mainchar.debug_showcolision()
            self.bookshelf1.debug_showcolision()
            self.bookshelf2.debug_showcolision()
            

    def interacting(self):
        self.tugging = not self.tugging
        self.sound.ToggleMusic()

    def toon_updateloop(self, task):
        self.mainchar.update_move()#Updates player movement
        return task.cont