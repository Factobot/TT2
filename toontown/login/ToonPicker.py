from direct.gui.DirectGui import *
from panda3d.core import *
from toontown.login.ToonPick import *
from PickerGlobals import *
from toontown.toonbase import TTLocalizer, ToontownGlobals
from toontown.toon import Toon

class ToonPicker:

    def __init__(self, avList, doneEvent):
        self.doneEvent = doneEvent
        self.currentSelection = None
        self.background = OnscreenImage(
            image = loader.loadTexture("stage_3/maps/t2_gui_pat_bg.png"),
        )
        
        self.background.reparentTo(render2dp, NO_FADE_SORT_INDEX)
        self.title = OnscreenText(text=TTLocalizer.PickAToon,
            scale = (0.1),
            font = ToontownGlobals.getMickeyFont(),
            fg = Vec4(1,1,0,1),
            pos = (0,0.9)
        )
        
        self.title.reparentTo(aspect2dp)
        self.profileBg = OnscreenImage(
            image = loader.loadTexture("stage_3/maps/t2_gui_pat_profile.png"),
            pos = Vec3(0.9, 0, -0.1),
            scale = (0.8, 1, 0.9)
        )
        
        self.profileBg.setTransparency(TransparencyAttrib.MAlpha)
        self.profileBg.reparentTo(aspect2dp)
        self.notChosen = OnscreenText(text=TTLocalizer.NoToonChosen,
            scale = (0.2),
            parent = self.profileBg,
            font = ToontownGlobals.getMickeyFont(),
            fg = Vec4(0,0.6,1,1),
            wordwrap = 5
        )
        self.playButton = DirectButton(
            image = loader.loadTexture("stage_3/maps/t2_gui_confirm.png"),
            scale = (0.2),
            pos = (0.8,0,-0.7),
            parent = self.profileBg,
            relief = None,
            command = self.__handleToonPlay
        )
        self.playButton.hide()
        
        self.picks = []
        for i in range(NUM_TOONS):
            pick = ToonPick(self, i)
            pick.load()
            pick.hide()
            self.picks.append(pick)
        
        for av in avList:
            self.picks[avList.index(av)].setToon(av)
        
        for pick in self.picks:
            if pick.mode == MODE_NONE:
                pick.setCreate()
                
        self.pToon = Toon.Toon()
        self.pToon.reparentTo(self.profileBg)
        self.pToon.hide()
        
        self.background.hide()
        self.profileBg.hide()
        self.title.hide()
        
    def enter(self):
        self.background.show()
        self.profileBg.show()
        self.title.show()
        for pick in self.picks:
            pick.show()
    
    def exit(self):
        self.background.hide()
        self.profileBg.hide()
        self.title.hide()
        self.pToon.cleanup()
        base.audioManager.stopMusic()
        for pick in self.picks:
            pick.destroy()
            
    def setCurrentSelection(self, avId):
        self.currentSelection = avId
            
    def doPreview(self, toonDna):
        self.notChosen.hide()
        self.playButton.show()
        self.pToon.setDNA(toonDna)
        self.pToon.setScale(0.25)
        self.pToon.setDepthTest(1)
        self.pToon.setDepthWrite(1)
        self.pToon.setH(180)
        self.pToon.setPos(0,0,-0.6)
        self.pToon.loop("neutral")
        self.pToon.show()
        
    def __handleToonPlay(self):
        if self.currentSelection:
            print "indeed"
            messenger.send(self.doneEvent, [self.currentSelection, None, "choose"])
        
    def requestCreateAvatar(self, pick):
        messenger.send(self.doneEvent, [None, pick.slot, "create"])
        
