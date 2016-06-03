from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from panda3d.core import *
from PickerGlobals import *
from toontown.toonbase import ToontownGlobals, TTLocalizer
import random

class ToonPick:

    def __init__(self, picker, slot):
        self.picker = picker
        self.slot = slot
        self.mode = MODE_NONE
        
    def hide(self):
        self.bubble.hide()
        
    def show(self):
        self.bubble.show()
        
    def destroy(self):
        self.bubble.remove()
        
    def load(self):
        self.bubble = DirectButton(
            image = loader.loadTexture("stage_3/maps/t2_gui_pat_pick.png"),
            pos = Vec3(*PICK_POSITIONS[self.slot]),
            scale = (0.2),
            relief = None,
            text = TTLocalizer.MakeAToon,
            text_font = ToontownGlobals.getMickeyFont(),
            text_scale = (0.4),
            text_wordwrap = 5,
            text_fg = Vec4(0,0.5,1,1),
            command = self.__click
        )
        
        self.bubble.bind(DGG.WITHIN, self.__hover)
        self.bubble.bind(DGG.WITHOUT, self.__out)
        self.bubble.setTransparency(TransparencyAttrib.MAlpha)
        self.bubble.reparentTo(aspect2dp, NO_FADE_SORT_INDEX)
        
    def setCreate(self):
        if self.mode != MODE_NONE:
            return
            
        self.mode = MODE_CREATE
        
        
    def setToon(self, av):
        if self.mode != MODE_NONE:
            return
            
        self.mode = MODE_CHOOSE
        self.av = av
        name = av.name
        dna = av.dna
        # todo: load toon head
        
    def __click(self):
        if self.mode == MODE_CREATE:
            self.picker.requestCreateAvatar(self)
        
    def __hover(self, e):
        self.bubble["text_fg"] = Vec4(0,0.9,1,1)
        self.bubble.setScale(0.22)
        
    def __out(self, e):
        self.bubble["text_fg"] = Vec4(0,0.5,1,1)
        self.bubble.setScale(0.2)