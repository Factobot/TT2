from panda3d.core import *
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.showbase.DirectObject import *
from toontown.toonbase import ToontownGlobals

class ToonGUI(NodePath, DirectObject):
    dir = 0
    def __init__(self):
        NodePath.__init__(self, "ToonPlayerGUI")
        self.chatSlideIv = None
        
    def load(self):
        self.chatNode = base.a2dTopLeft.attachNewNode("ChatNode")
        self.chatNode.setPos(-1,0,-0.145)
        self.chatGui = OnscreenImage(
            "stage_3/maps/t2_gui_gp_cbg.png",
            parent = self.chatNode,
            scale = (0.9,1,0.25),
            pos = (0,0,0)
        )
        self.chatGui.setTransparency(TransparencyAttrib.MAlpha)
        self.closeButton = DirectButton(
            image = (loader.loadTexture("stage_3/maps/t2_gui_gp_close.png"), "stage_3/maps/t2_gui_gp_close_h.png"),
            parent = self.chatGui,
            relief = None,
            scale = (0.12,1,0.33),
            pos = (-0.83,0,-0.33),
            command = self.toggleChat
        )
        self.sendChatButton = DirectButton(
            image = (loader.loadTexture("stage_3/maps/t2_gui_gp_sc.png"), "stage_3/maps/t2_gui_gp_sc_h.png"),
            parent = self.chatGui,
            relief = None,
            scale = (0.1,1,0.34),
            pos = (0.81,0,-0.12)
            
        )
        self.sendSChatButton = DirectButton(
            image = (loader.loadTexture("stage_3/maps/t2_gui_gp_scp.png"), "stage_3/maps/t2_gui_gp_scp_h.png"),
            parent = self.chatGui,
            relief = None,
            scale = (0.08,1,0.21),
            pos = (0.9,0,0.11)
        )
        self.chatInput = DirectEntry(
            entryFont = loader.loadFont("stage_3/models/fonts/AnimGothic"),
            width = 15,
            cursorKeys = 1,
            focus = 1,
            scale = (0.1,1,0.3),
            text_align = TextNode.ALeft,
            frameColor = Vec4(0),
            pos = (-0.7,0,-0.2),
            parent = self.chatGui,
            command = self.__handleChatTyped
        )
        self.chatNode.stash()
        
    def __handleChatTyped(self, chat):
        if not self.dir:
            pass
        
    def enable(self):
        self.chatNode.unstash()
        self.accept(ToontownGlobals.ChatHotkey, self.toggleChat)
        
    def toggleChat(self):
        if not self.dir:
            self.ignore(ToontownGlobals.ChatHotkey)
            self.accept("escape", self.toggleChat)
            base.playAssistant.disableAvatarControls()
            self.chatInput.enterText("")
        else:
            self.ignore("escape")
            self.accept(ToontownGlobals.ChatHotkey, self.toggleChat)
            base.playAssistant.enableAvatarControls()
        self.toggleChatSlide()
        
    def toggleChatSlide(self):
        if self.chatSlideIv:
            self.chatSlideIv.finish()
            self.chatSlideIv = None
        finalX = 0.9 if not self.dir else -1
        self.dir = not self.dir
        def __done(): self.chatSlideIv = None
        self.chatSlideIv = Sequence(
            self.chatNode.posInterval(0.3, (finalX,0,self.chatNode.getZ())),
            Func(__done)
        )
        self.chatSlideIv.start()
            
            
            
            
            
            