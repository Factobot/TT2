from panda3d.core import *
from toontown.toon.ToonDNA import *
from toontown.makeatoon.MakeAToonSpaceGUI import MakeAToonSpaceGUI
from toontown.makeatoon.MakeAToonCamera import MakeAToonCamera
from toontown.toon.Toon import Toon
from toontown.toon.ToonDNA import ToonDNA
from toontown.toongui import Dialog
from toontown.toonbase import TTLocalizer, ToontownGlobals
from direct.gui.DirectGui import *
from direct.fsm.FSM import *
from direct.interval.IntervalGlobal import *

class MakeAToon(FSM):
    Stages = [
        "ChooseGender",
        "PickBody",
        "PickColor",
        "BirthMovie",
        "SetClothes",
        "SetName"
    ]
    def __init__(self, slot, doneEvent):
        FSM.__init__(self, "MakeAToon")
        self.slot = slot
        self.doneEvent = doneEvent
        self.currentStage = -1
        self.spaceGui = MakeAToonSpaceGUI(self)
        self.cameraWork = MakeAToonCamera(self)
        self.toon = None
        
    def skipMakeAToon(self):
        name = 'Skid'
        dna = ToonDNA()
        messenger.send(self.doneEvent, [self.slot, name, dna])
        
    def __load(self):
        base.cam.setPosHpr(-11.59, -19.19, 5.31, 329.74, 350.54, 0.00)
        self.room = loader.loadModel("phase_3/models/makeatoon/tt_m_ara_mat_room")
        remove = ["colorAll", "nameAll", "bodyAll", "cothAll", "camera_arrow", "spotlight", 
        "genderProps"]
        for r in remove:
            self.room.find("**/%s*" %r).removeNode()
        self.room.reparentTo(render)
        self.room.setScale(1.3,1.4,1)
        
        self.toon = Toon()
        
        self.table = loader.loadModel("stage_3/models/props/MAT_table")
        self.table.reparentTo(render)
        self.table.setScale(0.5)
        self.table.setPosHprScale(-5.13, 6.21, 0.00, 202.62, 0.00, 0.00, 0.50, 0.50, 0.50)
        self.notebook = self.table.attachNewNode(CardMaker("notebook").generate())
        self.notebook.setTwoSided(1)
        self.notebook.setPosHprScale(0.95,2.87,7.64,180,294,0,4,1,5)
        self.closet = loader.loadModel("phase_5.5/models/estate/closetBoy")
        self.closet.reparentTo(render)
        self.closet.setPos(7.12, 6.21, 0)
        self.closet.setH(-90)
        
        self.spaceGui.load(self.notebook)
        self.nameGui = aspect2dp.attachNewNode("MAT_NameGUI")
        self.namePanel = OnscreenImage(
            image = loader.loadTexture("stage_3/maps/t2_gu_mat_nameInput.png"),
            parent = self.nameGui,
            scale = (0.8,1,0.18)
        )
        self.namePanel.setTransparency(TransparencyAttrib.MAlpha)
        self.namePTitle = OnscreenText(text = TTLocalizer.TypeYourName,
            font = ToontownGlobals.getMickeyFont(),
            scale = .15,
            fg = (0,0.5,1,1),
            pos = (0,0.1)
        )
        self.namePTitle.reparentTo(self.nameGui, 1000)
        self.nameInput = DirectEntry(
            entryFont = ToontownGlobals.getToonFont(),
            width = 14,
            cursorKeys = 1,
            focus = 1,
            scale = .1,
            relief = DGG.SUNKEN,
            text_align = TextNode.ACenter,
            borderWidth=(0.01, 0.01),
            frameColor = Vec4(1),
            pos = (0,0,-0.07),
            command = self.__handleNameDone
        )
        self.nameInput.reparentTo(self.nameGui, 1000)
        self.submitButton = DirectButton(image=loader.loadTexture("stage_3/maps/t2_gui_confirm.png"),
            scale = .1,
            pos=(0.75,0,-0.18),
            relief=None,
            command=self.__handleNameDone
        )
        self.submitButton.setTransparency(TransparencyAttrib.MAlpha)
        self.submitButton.reparentTo(self.nameGui, 1000)
        self.nameGui.stash()

    def enter(self):
        #base.audioManager.stopMusic()
        #base.playMusic('stage_3/audio/bgm/MAT_Theme.mp3', True, volume=0.6)
        self.__load()
        self.request("ChooseGender")
        
    def exit(self):
        pass
        
    def enterChooseGender(self):
        self.spaceGui.request("Clean")
        self.currentStage = self.Stages.index("ChooseGender")
        if self.cameraWork.currentCam != "":
            self.cameraWork.request("ChooseGenderCamera")
        self.spaceGui.nextButton.hide()
        self.spaceGui.backButton.hide()
        self.genderDialog = Dialog.Dialog("", 
            title = TTLocalizer.ChooseAGender, flag = Dialog.CLOSE, doneEvent="genderDone")
        self.genderDialog.confirmButton.hide()
        boyButton = DirectButton(
            image = loader.loadTexture("stage_3/maps/t2_gui_boyChoice.png"),
            scale = (0.2,1,0.3),
            pos = (0.2,0,0),
            relief = None,
            parent = self.genderDialog.background,
            command = self.__handleGenderDone,
            extraArgs = ["m"]
        )
        girlButton = DirectButton(
            image = loader.loadTexture("stage_3/maps/t2_gui_girlChoice.png"),
            scale = (0.2,1,0.3),
            pos = (-0.2,0,0),
            relief = None,
            parent = self.genderDialog.background,
            command = self.__handleGenderDone,
            extraArgs = ["f"]
        )
        self.accept("genderDone", self.__handleGenderDone)
        
    def exitChooseGender(self):
        self.spaceGui.backButton.hide()
        self.spaceGui.nextButton.hide()
        self.genderDialog.destroy()
        
    def setGender(self, gender):
        self.gender = gender
        dna = ToonDNA()
        dna.newToonRandom(gender=gender)
        self.toon.setDNA(dna)
        self.toon.useLOD('1000')
        self.toon.stopLookAroundNow()
        self.toon.stopBlink()
        
    def __handleGenderDone(self, result):
        if result == "cancel":
            self.genderDialog.destroy()
            self.exit()
        elif result in ["m", "f"]:
            self.setGender(result)
            self.spaceGui.prepareToon()
            self.request("PickBody")
        
    def enterPickBody(self):
        self.currentStage = self.Stages.index("PickBody")
        self.spaceGui.request("BodyGUI")
        self.cameraWork.request("BodyPickCamera")
        
    def handleNext(self):
        length = len(self.Stages) - 1
        if self.currentStage < length:
            self.request(self.Stages[self.currentStage + 1])
        
    def handlePrev(self):
        if self.currentStage > 0:
            self.request(self.Stages[self.currentStage - 1])
            
    def enterPickColor(self):
        self.currentStage = self.Stages.index("PickColor")
        self.spaceGui.request("ColorGUI")
        
    def __prepareSquishToon(self):
        self.spaceGui.vt__altBuffer.setActive(0)
        self.toon.reparentTo(render)
        self.toon.setPos(self.table.getPos())
        self.originalToonScale = self.toon.getScale()
        self.toon.setPosHprScale(-4.65, 6.21, 4.13, -120, 0.00, 0.00, 2, 2, 0.02)
        self.toon.hide()
        
    def __unsquishToon(self):
        unsquish = self.toon.scaleInterval(1, self.originalToonScale)
        goto = ProjectileInterval(self.toon, duration=1, endPos=(0, 6.21, 0))
        rot = self.toon.hprInterval(1, (-180,0,0))
        allPar = Parallel(Func(self.toon.show), 
            Func(self.tableShakeIv.finish),
            rot, 
            unsquish, 
            goto,
            Func(self.spaceGui.vt__altBuffer.setActive, 1)
        )
        gotoWdb = Parallel(
            Func(self.toon.loop, 'walk'),
            self.toon.hprInterval(2, (-90,0,0)),
            self.toon.posInterval(2, (self.closet.getX() - 4, 6.21, 0))
        )
        self.unsquishToonIv = Sequence(allPar, 
            Wait(0.1), 
            Func(self.toon.loop, 'neutral'),
            Wait(0.4),
            self.toon.actorInterval('confused'),
            gotoWdb,
            self.toon.hprInterval(1, (-180,0,0)),
            Func(self.toon.loop, 'neutral'),
            Wait(0.5),
            Func(self.__birthMovieDone)
        )
        self.unsquishToonIv.start()
        
    def enterBirthMovie(self):
        self.currentStage = self.Stages.index("BirthMovie")
        self.spaceGui.request("Clean")
        self.toon.loop("jump-idle")
        self.tableShakeIv = Sequence(
            self.table.hprInterval(0.2, (204.62, 0, 0)),
            self.table.hprInterval(0.2, (202.62, 0, 0))
        )
        self.birthMovieSeq = Sequence(
            Func(self.tableShakeIv.loop),
            Wait(1),
            Func(self.cameraWork.request, "ToonPopCamera"),
            Wait(2.5),
            Func(self.__prepareSquishToon),
            Func(self.__unsquishToon)
        )
        self.birthMovieSeq.start()
        
    def __birthMovieDone(self):
        self.request("SetClothes")
        
    def enterSetClothes(self):
        self.currentStage = self.Stages.index("SetClothes")
        if self.cameraWork.currentCam != "cloth_cam":
            self.cameraWork.request("ClothesCamera")
        else:
            self.ccCamDone()
        
    def ccCamDone(self):
        self.spaceGui.request("Clothes")
        
    def enterSetName(self):
        self.currentStage = self.Stages.index("SetName")
        self.spaceGui.request("Clean")
        self.spaceGui.backButton.show()
        self.nameGui.unstash()
        
    def exitSetName(self):
        self.nameGui.stash()
        
    def __handleNameDone(self, name = None):
        if not name:
            name = self.nameInput.get()
        messenger.send(self.doneEvent, [self.slot, name, self.toon.style])

    def exit(self):
        base.audioManager.stopMusic()
        base.cam.setPosHpr(0,0,0,0,0,0)
        self.room.removeNode()
        self.toon.remove()
        self.table.removeNode()
        self.notebook.removeNode()
        self.closet.removeNode()
        self.spaceGui.unload()
        self.nameGui.removeNode()
        
        