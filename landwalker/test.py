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

#Embedded file name: toontown

from toontown.interaction.InteractiveObjectManager import *
base.interactiveObjectMgr = InteractiveObjectManager()

if 1:
    from direct.stdpy import threading, thread
    import sys

    def __inject_wx(_):
        code = textbox.GetValue()
        exec (code, globals())

    def openInjector_wx():
        import wx
        
        app = wx.App(redirect = False)
            
        frame = wx.Frame(None, title = "TTR Injector", size=(640, 400), style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.MINIMIZE_BOX)
        panel = wx.Panel(frame)
        button = wx.Button(parent = panel, id = -1, label = "Inject", size = (50, 20), pos = (295, 0))
        global textbox
        textbox = wx.TextCtrl(parent = panel, id = -1, pos = (20, 22), size = (600, 340), style = wx.TE_MULTILINE)
        frame.Bind(wx.EVT_BUTTON, __inject_wx, button)

        frame.Show()
        app.SetTopWindow(frame)
        
        textbox.AppendText("")
        
        threading.Thread(target = app.MainLoop).start()
        

    openInjector_wx()



loadPrcFileData("", "default-model-extension .bam")
        
ground = loader.loadModel('phase_4/models/neighborhoods/toontown_central')#("phase_6/models/neighborhoods/donalds_dock")
ground.reparentTo(render)

#boat = ground.find('**/donalds_boat')
#boat.setPos(-70, -40.2601, -5)

#water = ground.find('**/water')
#water.setTransparency(1)
#water.setColor(1, 1, 1, 0.8)
base.cTrav = CollisionTraverser("base.cTrav")
dna = ToonDNA()
dna.newToonFromProperties('dss',
      'ms',
      'm',
      'm',
      17,
      0,
      17,
      17,
      3,
      3,
      3,
      3,
      7,
2)
     

toon = Toon()
toon.setDNA(dna)
toon.reparentTo(render)
toon.setX(-84)
toon.setY(65.9284)
toon.setZ(3.27964)
toon.setH(-45.1308)
toon.setName("Not Flippy")     

toon = Toon()
toon.setDNA(dna)
toon.reparentTo(render)
toon.setX(-84)
toon.setY(65.9284)
toon.setZ(3.27964)
toon.setH(-45.1308)
toon.setName("Flippy")

def setAnimState(st):
    if toon.animFSM.getCurrentState().getName() != st:
        toon.animFSM.request(st)
        
toon.b_setAnimState = setAnimState

assistant = base.playAssistant = PlayAssistant(toon)
assistant.setup()
assistant.request("Play")

def printPos():
 pos = toon.getPos()
 print(str(pos))
 
def printHpr():
 hpr = toon.getHpr()
 print(str(hpr))
 
music = loader.loadMusic("stage_3/audio/bgm/ToontropolisTheme.wav")
music.setLoop(1)
#music.play()


#base.oobe()
base.accept("f1", printPos, [])
base.accept("f2", printHpr, [])
base.disableMouse()
base.camLens.setFilmSize(*ToontownGlobals.FilmSize)
base.camLens.setFov(52.0)
base.camLens.setFar(400.0)
base.camLens.setNear(1.0)
run()


