from glob import glob
import props
from panda3d.core import Point3
stacks = []
stacklocations = [Point3(0,30,0),
Point3(0,-20,0)]
def debug_showcolision():
    global stacks
    for obj in stacks:
        obj.debug_showcolision()

class stack(props.propos):
    StackID = 0
    def __init__(self,base,pos):
        global stacks
        super().__init__(base,0,pos, cname= "StackColider", isactor= True)
        self.StackID = len(stacks)
    
    def topple(self):
        pass

    def destroy(self):
        global stacks
        stacks.remove(self)
        super().destroy()
        
        
        