from direct.gui.DirectGui import *
from panda3d.core import *
from toontown.login.ToonPick import *
from PickerGlobals import *
from toontown.toonbase import TTLocalizer, ToontownGlobals

class ToonPicker:

    def __init__(self, avList, doneEvent):
        self.doneEvent = doneEvent
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
        
        self.title.reparentTo(aspect2dp, NO_FADE_SORT_INDEX)
        self.profileBg = OnscreenImage(
            image = loader.loadTexture("stage_3/maps/t2_gui_pat_profile.png"),
            pos = Vec3(0.9, 0, -0.1),
            scale = (0.8, 1, 0.9)
        )
        
        self.profileBg.setTransparency(TransparencyAttrib.MAlpha)
        self.profileBg.reparentTo(aspect2dp, NO_FADE_SORT_INDEX)
        self.notChosen = OnscreenText(text=TTLocalizer.NoToonChosen,
            scale = (0.2),
            parent = self.profileBg,
            font = ToontownGlobals.getMickeyFont(),
            fg = Vec4(0,0.6,1,1),
            wordwrap = 5
        )
        
        self.picks = []
        for i in range(NUM_TOONS):
            pick = ToonPick(self, i)
            pick.load()
            pick.hide()
            self.picks.append(pick)
        
        for av in avList:
            self.picks[av.slot].setToon(av)
        for pick in self.picks:
            if pick.mode == MODE_NONE:
                pick.setCreate()
        
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
        for pick in self.picks:
            pick.destroy()
        
    def requestCreateAvatar(self, pick):
        messenger.send(self.doneEvent, [None, pick.slot, "create"])
        
