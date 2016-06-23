from panda3d.core import *
from direct.gui.DirectGui import *

from toontown.interaction.InteractiveObject import *
from toontown.toonbase import ToontownGlobals
import NametagGlobals

class Nametag(NodePath, InteractiveObject):
    def __init__(self, parent, properties = NametagGlobals.ToonNametagProps):
        NodePath.__init__(self, "Nametag")
        InteractiveObject.__init__(self, INTERACTIVE_NAMETAG)
        self.parent = parent
        self.properties = properties
        
    def load(self):
        self.tagFrame = loader.loadModel('phase_3/models/props/panel').copyTo(self)#(CardMaker(NodePath.getName(self)).generate())
        self.tagFrame.setTransparency(1)
        self.tagFrame.setColor(self.properties["fg"])
        self.tagFrameText = self.attachNewNode(TextNode(NodePath.getName(self)))
        self.tagFrameText.node().setFont(loader.loadFont("stage_3/models/fonts/AnimGothic"))
        self.tagFrameText.node().setAlign(TextNode.ACenter)
        self.tagFrameText.node().setWordwrap(7.5)
        self.tagFrameText.setScale(0.3)
        self.tagFrameText.setPos(0,-0.025,0)
        self.tagFrameText.setColor(self.properties["textColor"])
        self.reparentTo(self.parent)
        self.setBillboardPointEye()
        self.stash()
        
    def setName(self, name):
        self.tagFrameText.node().setText(name)
        width = self.tagFrameText.node().getWidth() * 0.3
        height = self.tagFrameText.node().getHeight() * 0.3
        self.tagFrame.setX((self.tagFrameText.node().getLeft()+self.tagFrameText.node().getRight())/2.0)
        self.tagFrame.setZ(((self.tagFrameText.node().getTop()+self.tagFrameText.node().getBottom())*0.3)/2)
        self.tagFrame.setScale(width + 0.2, 1, height + 0.04)
        self.tagFrameText.setZ(0)
        InteractiveObject.enable(self)
        self.unstash()
        
        
        
        
        
        
        
        