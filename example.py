import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from panda3d.core import *

# Add some text
bk_text = "This is my Demo"
textObject = OnscreenText(text=bk_text, pos=(0.95, -0.95), scale=0.07,
                          fg=(1, 0.5, 0.5, 1), align=TextNode.ACenter,
                          mayChange=1)

# Callback function to set text
def incBar(arg):
    if (bar['value'] + arg >= 100):
        bar['value'] = 100
    elif (bar['value'] + arg <= 0):
        bar['value'] = 0
    else:
        bar['value'] += arg
    bar.setText("Progress is: " + str(int(bar['value'])) + '%')
    #textObject.setText(text)

# Create a frame
frame = DirectFrame(text="main", scale=0.001)
# Add button
bar = DirectWaitBar(text="None", value=50, pos=(0, .4, .4), hpr=(0,0,0))
bar.setText("nah")
# Create 4 buttons
button_1 = DirectButton(text="+1", scale=0.05, pos=(-.3, .6, 0),
                        command=incBar, extraArgs=[1])
button_10 = DirectButton(text="+10", scale=0.05, pos=(0, .6, 0),
                         command=incBar, extraArgs=[10])
button_m1 = DirectButton(text="-1", scale=0.05, pos=(0.3, .6, 0),
                         command=incBar, extraArgs=[-1])
button_m10 = DirectButton(text="-10", scale=0.05, pos=(0.6, .6, 0),
                          command=incBar, extraArgs=[-10])

# Run the tutorial
def updateloop(task):
    incBar(1/2 * globalClock.getDt())
    return task.cont

base.taskMgr.add(updateloop,"updatetest")
base.run()