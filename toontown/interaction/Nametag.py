from panda3d.core import *
from direct.gui.DirectGui import *

from toontown.interaction.InteractiveObject import *
from toontown.toonbase import ToontownGlobals
from toontown.interaction.Nametag2D import Nametag2D
import NametagGlobals
import math

class Nametag(NodePath, InteractiveObject):
    def __init__(self, avatar, parent, properties = NametagGlobals.ToonNametagProps):
        NodePath.__init__(self, "Nametag")
        InteractiveObject.__init__(self, INTERACTIVE_NAMETAG)
        self.avatar = avatar
        self.parent = parent
        self.name = None
        self.cellData = None
        self.properties = properties
        
    def load(self):
        self.tagFrame = loader.loadModel('phase_3/models/props/panel').copyTo(self)#(CardMaker(NodePath.getName(self)).generate())
        self.tagFrame.setTransparency(1)
        self.tagFrame.setColor(self.properties["fg"])
        self.tagFrameText = self.attachNewNode(TextNode(NodePath.getName(self)))
        self.tagFrameText.node().setFont(loader.loadFont("stage_3/models/fonts/AnimGothic"))
        self.tagFrameText.node().setAlign(TextNode.ACenter)
        self.tagFrameText.node().setWordwrap(7.5)
        self.tagFrameText.setScale(0.33)
        self.tagFrameText.setPos(0,-0.025,0)
        self.tagFrameText.setColor(self.properties["textColor"])
        self.pointArrow = loader.loadModel('phase_3/models/props/arrow')
        self.pointArrow.setScale(0.5)
        self.pointArrow.setColor(self.properties["arrowColor"])
        self.reparentTo(self.parent)
        self.stash()
        
    def __makeBillboard(self):
        self.setEffect(BillboardEffect.make(
                Vec3(0,0,1),
                True,
                False,
                1.0,
                base.camera,
                Point3(0,0,0)))

    def __clearBillboad(self):
        self.clearEffect(BillboardEffect)
        
    def unload(self):
        InteractiveObject.disable(self)
        if self.cellData:
            self.availableScreenCell(*self.cellData)
            self.cellData = None
        self.nametag2d.reparentTo(hidden)
        self.nametag2d.removeNode()
        self.removeNode()
        
    def updateScreenNametag(self):
        if self.avatar == base.localAvatar:
            return
        if not self.name:
            return
        if self.avatar.isEmpty() or not self.avatar:
            return
        loc = self.avatar.getPos(base.localAvatar)
        rot = base.localAvatar.getQuat(base.camera)
        cSpace = rot.xform(loc)
        radians = math.atan2(cSpace[0], cSpace[1])
        degrees = radians / math.pi * 180
        d2 = degrees
        if d2 < 0: d2 *= -1
        if d2 >= 70:
            if not self.cellData and self.enabled:
                cell = self.getScreenCell()
                if not cell:
                    return
                parent, pos = cell
                self.cellData = [parent, pos]
                self.nametag2d.reparentTo(parent)
                self.nametag2d.setPos(*pos)
            self.pointArrow.setR(degrees - 90)
        else:
            if self.cellData:
                self.nametag2d.reparentTo(hidden)
                self.availableScreenCell(*self.cellData)
                self.cellData = None
        
    def setName(self, name):
        self.__clearBillboad()
        self.name = name
        self.tagFrameText.node().setText(name)
        width = self.tagFrameText.node().getWidth() * 0.3
        height = self.tagFrameText.node().getHeight() * 0.3
        self.tagFrame.setX((self.tagFrameText.node().getLeft()+self.tagFrameText.node().getRight())/2.0)
        self.tagFrame.setZ(((self.tagFrameText.node().getTop()+self.tagFrameText.node().getBottom())*0.3)/2)
        self.tagFrame.setScale(width + 0.3, 1, height + 0.05)
        self.tagFrameText.setZ(0)
        self.__genNametag2d()
        self.__makeBillboard()
        InteractiveObject.enable(self)
        self.unstash()
        
    def __genNametag2d(self):
        if self.cellData:
            self.pointArrow.reparentTo(hidden)
            self.nametag2d.removeNode()
            self.availableScreenCell(*self.cellData)
            self.cellData = None
        self.nametag2d = Nametag2D(self)
        
    def triggerChat(self, balloon):
        pass
        
        