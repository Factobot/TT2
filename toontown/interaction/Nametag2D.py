from panda3d.core import *

class Nametag2D(NodePath):
    def __init__(self, nametag):
        NodePath.__init__(self, "Nametag2D")
        self.nametag = nametag
        self.nametagNode = self.nametag.copyTo(hidden)
        self.nametagNode.reparentTo(self)
        self.pointArrow = self.nametag.pointArrow
        self.pointArrow.reparentTo(self)
        sz = -(self.nametag.tagFrameText.node().getHeight() * 0.3) -0.2
        self.pointArrow.setZ(sz)
        