import direct.directbase.DirectStart
from panda3d.core import *
from direct.controls import GravityWalker
from direct.fsm.FSM import *
from toontown.toon.Toon import Toon
from toontown.toon.ToonDNA import ToonDNA
from toontown.toonbase import ToontownGlobals
from toontown.controls import InteractiveCameraDriver
from toontown.controls import ToontownControlManager

loadPrcFileData("", "default-model-extension .bam")
#loadPrcFileData("", "want-WASD 1")

class PlayAssistant(FSM):
    wantLegacyLifter = False
    avatarRadius = 1.4
    floorOffset = ToontownGlobals.FloorOffset
    reach = 4.0
    offset = 3.2375
    def __init__(self, toon):
        FSM.__init__(self, "PlayAssistant")
        self.toon = toon
        self.controlManager = ToontownControlManager.ToontownControlManager()
        self.cameraDriver = InteractiveCameraDriver.InteractiveCameraDriver(base.camera)
        self.cTrav = CollisionTraverser('base.cTrav')
        self.keyData = {"w":0, "a":0, "s":0, "d":0, "space":0}
        
    def setup(self):
        self.setupWalk()
        
    def setupWalk(self):
        gravityWalker = GravityWalker.GravityWalker(gravity=32.174, legacyLifter=self.wantLegacyLifter)
        gravityWalker.setWallBitMask(ToontownGlobals.WallBitmask)
        gravityWalker.setFloorBitMask(ToontownGlobals.FloorBitmask)
        gravityWalker.initializeCollisions(self.cTrav, self.toon, self.avatarRadius, self.floorOffset, self.reach)
        gravityWalker.setAirborneHeightFunc(self.getAirborneHeight)
        self.controlManager.add(gravityWalker, 'walk')
        self.physControls = gravityWalker
        
        self.controlManager.use("walk", self.toon)
        self.controlManager.disable()
        
    def getAirborneHeight(self):
        return self.offset + 0.025000000000000001
        
    def setNormalSpeeds(self):
        self.controlManager.setSpeeds(ToontownGlobals.ToonForwardSpeed, ToontownGlobals.ToonJumpForce, ToontownGlobals.ToonReverseSpeed, ToontownGlobals.ToonRotateSpeed)
        
    def enableInteractiveCamera(self):
        self.cameraDriver.setTarget(self.toon)
        self.cameraDriver.start()
        
    def activateWalkAnimations(self):
        self.accept("w", self.__toggleKey, ["w"])
        self.accept("w-up", self.__toggleKey, ["w"])
        self.accept("a", self.__toggleKey, ["a"])
        self.accept("a-up", self.__toggleKey, ["a"])
        self.accept("s", self.__toggleKey, ["s"])
        self.accept("s-up", self.__toggleKey, ["s"])
        self.accept("d", self.__toggleKey, ["d"])
        self.accept("d-up", self.__toggleKey, ["d"])
        self.accept("space", self.__toggleKey, ["space"])
        self.accept("space-up", self.__toggleKey, ["space"])
        taskMgr.add(self.__watchKeyTask, "watch-key")
        
    def deactivateWalkAnimations(self):
        self.ignore("w")
        self.ignore("a")
        self.ignore("s")
        self.ignore("d")
        self.ignore("space")
        taskMgr.remove("watch-key")
        
    def __watchKeyTask(self, task): # should be b_setAnim
        if self.keyData["w"]:
            if self.keyData["space"]:
                pass #self.toon.setAnimState(self.toon, "jumpRunning")
            else:
                self.toon.setAnimState(self.toon, "run")
            return task.cont
        elif self.keyData["a"] or self.keyData["d"] or self.keyData["s"]:
            if self.keyData["space"]:
                self.toon.setAnimState(self.toon, "jumpAirborne")
            else:
                self.toon.setAnimState(self.toon, "walk")
        elif self.physControls.isAirborne:
            self.toon.setAnimState(self.toon, "jumpAirborne")
        else:
            self.toon.setAnimState(self.toon, "neutral")
        
        return task.cont
        
    def __toggleKey(self, key):
        self.keyData[key] = not self.keyData[key]
        
    def enterPlay(self):
        self.setNormalSpeeds()
        self.controlManager.enable()
        self.activateWalkAnimations()
        self.enableInteractiveCamera()
        base.camera.setPos(0,-18,4)
        
        
ground = loader.loadModel("phase_6/models/neighborhoods/donalds_dock")
ground.reparentTo(render)
        
toon = Toon()
dna = ToonDNA('t\x11\x04\x00\x01\x00\x1b\x00\x1b\x00\x1b\x06\x00\x06\x06')
toon.setDNA(dna)
toon.reparentTo(render)

def setAnimState(self, st):
    if self.animFSM.getCurrentState().getName() != st:
        self.animFSM.request(st)
        
toon.setAnimState = setAnimState

assistant = PlayAssistant(toon)
assistant.setup()
assistant.request("Play")

#base.oobe()
base.disableMouse()
run()


