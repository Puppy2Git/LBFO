from glob import glob
import props
from panda3d.core import Point3
stacks = []#Stacks in play
#Stacks to be loaded in
stacklocations = [[Point3(0,30,0), 100],
[Point3(0,-20,0), 100],
[Point3(20,0,0), 100],
[Point3(-20,0,0), 100]
]
def debug_showcolision():
    global stacks
    for obj in stacks:
        obj.debug_showcolision()

class stack(props.propos):
    StackID = 0
    def __init__(self,base,pos, dificulty):
        global stacks
        self.resistance = dificulty
        super().__init__(base,0,pos, cname= "StackColider", isactor= True)
        self.StackID = len(stacks)
    
    def topple(self):
        '''
        Should do an animation and then destroy it's self
        '''
        self.destroy()
        

    def destroy(self):
        global stacks
        stacks.remove(self)
        super().destroy()
        
        
        