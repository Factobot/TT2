from panda3d.core import *
from direct.gui.DirectGui import *

from toontown.toonbase import ToontownGlobals
import ChatGlobals
import math

class ChatBalloon(NodePath):
    WORDWRAP = 10
    TEXT_SHIFT = (0.1, -0.05, 1.1)
    TEXT_SHIFT_PROP = 0.08
    NATIVE_WIDTH = 10.0
    MIN_WIDTH = 2.5
    BUBBLE_PADDING = 0.3
    BUBBLE_PADDING_PROP = 0.05
    BUTTON_SCALE = 6
    BUTTON_SHIFT = (-0.2, 0, 0.6)
    def __init__(self, avatar, nametag, properties = ChatGlobals.ToonChatProps):
        NodePath.__init__(self, "Balloon")
        self.avatar = avatar
        self.nametag = nametag
        self.chat = None
        self.properties = properties
        
    def load(self, isThought = 0, is2d = 0):
        if isThought:
            self.balloon = loader.loadModel('phase_3/models/props/chatbox_thought_cutout')
        elif is2d:
            self.balloon = loader.loadModel('phase_3/models/props/chatbox_noarrow')
        else:
            self.balloon = loader.loadModel('phase_3/models/props/chatbox')
        self.balloon.reparentTo(self)
        self.balloon.hide()
        self.textNode = self.attachNewNode(TextNode('text'))
        self.textNode.node().setFont(self.properties['font'])
        self.textNode.node().setWordwrap(self.WORDWRAP)
        self.reparentTo(self.nametag)
        
    def setChat(self, chat):
        if isinstance(chat, type(u'')):
            self.textNode.node().setWtext(chat)
        else:
            self.textNode.node().setText(chat)
        balloon = self.balloon
        top = balloon.find('**/top')
        middle = balloon.find('**/middle')
        bottom = balloon.find('**/bottom')
        width, height = self.textNode.node().getWidth(), self.textNode.node().getHeight()
        self.textNode.setAttrib(DepthWriteAttrib.make(0))
        self.textNode.setPos(self.TEXT_SHIFT)
        self.textNode.setX(self.textNode, self.TEXT_SHIFT_PROP*width)
        self.textNode.setZ(self.textNode, height)
        if width < self.MIN_WIDTH:
            width = self.MIN_WIDTH
            self.textNode.setX(self.textNode, width/2.0)
            self.textNode.node().setAlign(TextNode.ACenter)
            
        width *= 1+self.BUBBLE_PADDING_PROP
        width += self.BUBBLE_PADDING
        balloon.setSx(width/self.NATIVE_WIDTH)
        middle.setSz(height)
        top.setZ(top, height-1)
        self.balloon.show()
        self.nametag.triggerChat(self)
        
        