from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from panda3d.core import *
#Hanles GUI elements

class GuiManager():
    bar = None
    def __init__(self):
        self.bar = DirectWaitBar(text="0", value=0, pos=(0, .4, -0.9), hpr=(0,0,0), scale = (.5,1,1))
        self.bar.hide()
    
    def showProgressBox(self, state):
        '''
        Either shows or hides the progress bar given the value\n
        >>> GuiManager.showProgressBox(True)\n
        Shows the Bar
        '''
        if (state):
            self.bar.show()
        else:
            self.bar.hide()

    def setProgressBoxAmount(self, x):
        '''
        Sets the progress bar given the value as well as updating the text\n
        >>> GuiManager.setProgressBoxAmount(100)\n
        Sets the bar to full
        '''
        self.bar['value'] = x
        self.bar.setText("Progress is: " + str(int(self.bar['value'])) + '%')
    
    def getProgressBoxAmount(self):
        '''
        Gets the progress bar value\n
        >>> GuiManager.getProgressBoxAmount()\n
        Gives a value
        '''
        return self.bar['value']