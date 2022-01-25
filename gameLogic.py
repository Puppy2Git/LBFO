import imp
from direct.showbase.DirectObject import DirectObject
import ohmyears
from obstacles import stack
from props import propos
from ohmyears import soundManager
from props import getdir
from toons import state
from toons import controllerToon
from panda3d.core import Point3
from math import pi


class gameWorld(DirectObject):
    tugging = False
    debug = False
    def __init__(self, base, debug):
        self.base = base
        super().__init__()
        self.sound = soundManager(self.base)
        self.accept('TapeCollider', self.dothing)
        self.accept('Interacting',self.interacting)
        self.debug = debug

    def dothing(self, entry):
        print(entry)

    
    def initWorld(self):
        #Character
        self.mainchar = controllerToon(self.base, Point3(0,0,0),getdir('S'))
        self.movementstate = state(lambda : self.mainchar.canMove(move = 1),lambda : self.mainchar.canMove(move = 0))
        self.tuggingstate = state(lambda : self.mainchar.canTug(tug = 2), lambda : self.mainchar.canTug(tug = 0))
        self.movementstate.start()
        #Props
        self.bookshelf1 = propos(self.base,2,Point3(-20,10,0),getdir('S'),2)
        self.bookshelf2 = propos(self.base,2,Point3(10,10,0),getdir('S'),2)
        #Stacks
        self.stack = stack(base = self.base, pos = Point3(0,30,0))
        
        

        if (self.debug):
            self.mainchar.debug_showcolision()
            self.bookshelf1.debug_showcolision()
            self.bookshelf2.debug_showcolision()
            self.stack.debug_showcolision()
            

    def interacting(self):
        
        self.tugging = not self.tugging
        if (self.tugging):
            self.movementstate.end()
            self.tuggingstate.start()
        else:
            self.tuggingstate.end()
            self.movementstate.start()
            
        self.sound.ToggleMusic()

    def toon_updateloop(self, task):
        self.mainchar.update_move()#Updates player movement
        return task.cont