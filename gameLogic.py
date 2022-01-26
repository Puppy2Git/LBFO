import imp
from direct.showbase.DirectObject import DirectObject
import ohmyears
import obstacles
from ohmyears import soundManager
import props
import toons
from panda3d.core import Point3
from math import pi


class gameWorld(DirectObject):
    tugging = False
    debug = False
    stackColiding = False
    focus_stack = None
    def __init__(self, base, debug):
        self.base = base
        super().__init__()
        self.sound = soundManager(self.base)
        self.accept('TapeCollider-into-StackColider', self.stackColide, [True])
        self.accept('TapeCollider-exit-StackColider', self.stackColide, [False])
        self.accept('Interacting',self.interacting)
        self.accept("Full Stack", self.stackchecker)
        self.debug = debug

    def stackColide(self, state, entry):
        '''
        This is called when a collision event happens with a stack and the tape collision handler\n
        Sets the stack it collided with and if it is still coliding\n
        only should be called by the accept statement\n
        >>> self.accept('TapeCollider-into-StackColider', self.stackColide, [True])\n
        Starts collision and sets it target stack
        '''
        
        if (state):
            for obj in obstacles.stacks:
                if obj.nodePath == entry.getIntoNodePath():
                    self.focus_stack = obj
        self.stackColiding = state

    def stackchecker(self):
        '''
        Called when a stack has reached the highest pull ammount by the player\n
        This then destroys the stack and stops the tugging of the character\n
        the end\n
        '''
        self.interacting()
        self.focus_stack.destroy()
        self.focus_stack = None

    
    def initWorld(self):
        '''
        Used to initalize the gameworld\n
        Only should be called once in the main loop\n
        >>> my_game.initWorld()
        '''
        #Character
        self.mainchar = toons.controllerToon(self.base, Point3(0,0,0),props.getdir('S'))
        self.movementstate = toons.state(lambda : self.mainchar.canMove(move = 1),lambda : self.mainchar.canMove(move = 0))
        self.tuggingstate = toons.state(lambda : self.mainchar.canTug(tug = 2, looking = self.focus_stack.nodePath), lambda : self.mainchar.canTug(tug = 0, looking = self.focus_stack))
        self.movementstate.start()
        #Props
        self.addprops()
        #Stacks
        self.genstacks()
        
        
        if (self.debug):
            self.mainchar.debug_showcolision()
            props.debug_showcolision()
            obstacles.debug_showcolision()
    
    def addprops(self):
        '''
        Adds props given by the props list
        '''
        for location in props.proplocations:
            props.propos(self.base,location[0],location[1],location[2],location[3])
        


    def genstacks(self):
        '''
        Generate stacks given the locations specified in the list
        '''
        for location in obstacles.stacklocations:
            obstacles.stacks.append(obstacles.stack(base = self.base, pos = location))
    

    def interacting(self):
        '''
        Should be called from the Interacting event\n
        This handles the logic behind starting to tug\n
        >>> self.accept('Interacting',self.interacting)
        '''
        self.tugging = not self.tugging
        if (self.tugging and self.stackColiding):
            self.movementstate.end()
            self.tuggingstate.start()
            self.sound.ToggleMusic(True)
        else:
            self.tugging = False
            self.tuggingstate.end()
            self.movementstate.start()
            self.sound.ToggleMusic(False)
            

    def toon_updateloop(self, task):
        '''
        This is the main toon update loop\n
        This handles updating the movement of the toon\n
        '''
        self.mainchar.update_move()#Updates player movement
        return task.cont