from direct.gui.DirectGui import *
from panda3d.core import *
from toontown.toonbase import ToontownGlobals

CONFIRM = 0
CLOSE = 1

class Dialog(OnscreenImage):
    def __init__(self, message, title = 'Toontown 2', flag = CONFIRM, doneEvent = ''):
        self.background = OnscreenImage(
            image = loader.loadTexture("stage_3/maps/t2_gui_panelBg.png"),
            scale = (0.8,1,0.5),
            parent = aspect2dp
        )
        self.background.setTransparency(TransparencyAttrib.MAlpha)
        self.titleText = OnscreenText(
            text = title,
            font = ToontownGlobals.getToonFont(),
            parent = self.background,
            scale = (0.09,0.13,1),
            pos = (-0.85,0.77),
            fg = (1,1,0,1),
            align = TextNode.ALeft
        )
        self.messageText = OnscreenText(
            text = message,
            font = ToontownGlobals.getToonFont(),
            parent = self.background,
            scale = (0.13),
            pos = (-0.8,0.5),
            wordwrap=12,
            align = TextNode.ALeft
        )
        if flag == CLOSE:
            self.__createConfirm()
            self.__createClose()
        elif flag == CONFIRM:
            self.__createConfirm()
            
        self.doneEvent = doneEvent
            
    def destroy(self):
        self.background.removeNode()
            
    def __createConfirm(self):
        self.confirmButton = DirectButton(
            image = loader.loadTexture("stage_3/maps/t2_gui_confirm.png"),
            scale = (0.06,1,0.1),
            pos = (0.68,0,0.81),
            parent = self.background,
            relief = None,
            command = self.__handle,
            extraArgs = ["confirm"]
        )
            
    def __createClose(self):
        self.closeButton = DirectButton(
            image = loader.loadTexture("stage_3/maps/t2_gui_close.png"),
            scale = (0.06,1,0.1),
            pos = (0.83,0,0.81),
            parent = self.background,
            relief = None,
            command = self.__handle,
            extraArgs = ["close"]
        )
    
    def __handle(self, result):
        messenger.send(self.doneEvent, [result])
        
        
        