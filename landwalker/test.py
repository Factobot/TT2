import direct.directbase.DirectStart
from panda3d.core import *
from direct.controls import GravityWalker
from direct.fsm.FSM import *
from toontown.toon.Toon import Toon
from toontown.toon.ToonDNA import ToonDNA
from toontown.toonbase import ToontownGlobals
from toontown.controls import InteractiveCameraDriver
from toontown.controls import ToontownControlManager
from toontown.toon.PlayAssistant import PlayAssistant

loadPrcFileData("", "default-model-extension .bam")
        
ground = loader.loadModel("phase_6/models/neighborhoods/donalds_dock")
ground.reparentTo(render)
        
toon = Toon()
dna = ToonDNA('t\x11\x04\x00\x01\x00\x1b\x00\x1b\x00\x1b\x06\x00\x06\x06')
toon.setDNA(dna)
toon.reparentTo(render)

def setAnimState(st):
    if toon.animFSM.getCurrentState().getName() != st:
        toon.animFSM.request(st)
        
toon.b_setAnimState = setAnimState

assistant = PlayAssistant(toon)
assistant.setup()
assistant.request("Play")

#base.oobe()
base.disableMouse()
run()


