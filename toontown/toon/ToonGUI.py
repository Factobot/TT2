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
        self.chatGui = OnscreenImage(
            "stage_3/maps/t2_gui_gp_cbg.png",
            parent = self,
            scale = (1,1,1)
        )
        self.chatGui.setTransparency(TransparencyAttrib.MAlpha)
        '''
        self.chatInput = DirectEntry(
            entryFont = loader.loadFont("stage_3/models/fonts/AnimGothic"),
            width = 15,
            cursorKeys = 1,
            focus = 1,
            scale = .1,
            text_align = TextNode.ALeft,
            frameColor = Vec4(1),
            pos = (0,0,0.1),#-0.5),
            parent = self,
            command = self.__handleChatTyped
        )
        '''
        #self.chatGui.setX(-((self.chatGui.getWidth()/2)*.1))
        self.reparentTo(base.a2dBottomCenter)
        self.stash()
        
    def __handleChatTyped(self, chat):
        pass
        
    def enable(self):
        #self.unstash()
        self.accept(ToontownGlobals.ChatHotkey, self.toggleChatSlide)
        
    def toggleChatSlide(self):
        if self.chatSlideIv:
            self.chatSlideIv.finish()
            self.chatSlideIv = None
        finalZ = 0.1 if not self.dir else -0.5
        self.dir = not self.dir
        def __done(): self.chatSlideIv = None
        self.chatSlideIv = Sequence(
            self.chatGui.posInterval(0.3, (self.chatGui.getX(),0,finalZ)),
            Func(__done)
        )
        self.chatSlideIv.start()
            
            
            
            
            
            