import direct.directbase.DirectStart, random
from panda3d.core import *
loadPrcFileData("", "model-path resources/")
from direct.controls import GravityWalker
from direct.fsm.FSM import *
from toontown.toon.Toon import Toon
from toontown.toon.ToonDNA import ToonDNA
from toontown.toonbase import ToontownGlobals
from toontown.controls import InteractiveCameraDriver
from toontown.controls import ToontownControlManager
from toontown.toon.PlayAssistant import PlayAssistant

loadPrcFileData("", "default-model-extension .bam")
        
ground = loader.loadModel('phase_4/models/neighborhoods/toontown_central')#("phase_6/models/neighborhoods/donalds_dock")
ground.reparentTo(render)

#boat = ground.find('**/donalds_boat')
#boat.setPos(-70, -40.2601, -5)

#water = ground.find('**/water')
#water.setTransparency(1)
#water.setColor(1, 1, 1, 0.8)
        
dna1 = ToonDNA('t\x11\x04\x00\x01\x00\x1b\x00\x1b\x00\x1b\x06\x00\x06\x06')
dnaList = [dna1]
for i in range(10):
    dnaList.append(ToonDNA())
dna = random.choice(dnaList)

if dna == dna1:
 print("DNAManager: Got rare SillyPeppyMcSpeed DNA!")
        

toon = Toon()
toon.setDNA(dna)
toon.reparentTo(render)
toon.setX(-84)
toon.setY(65.9284)
toon.setZ(3.27964)
toon.setH(-45.1308)

def setAnimState(st):
    if toon.animFSM.getCurrentState().getName() != st:
        toon.animFSM.request(st)
        
toon.b_setAnimState = setAnimState

assistant = PlayAssistant(toon)
assistant.setup()
assistant.request("Play")

def printPos():
 pos = toon.getPos()
 print(str(pos))
 
def printHpr():
 hpr = toon.getHpr()
 print(str(hpr))


#base.oobe()
base.accept("f1", printPos, [])
base.accept("f2", printHpr, [])
base.disableMouse()
run()


