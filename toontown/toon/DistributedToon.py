from direct.distributed.DistributedSmoothNode import DistributedSmoothNode
from toontown.avatar.DistributedAvatar import DistributedAvatar
from toontown.toon.Toon import Toon
from toontown.toon.ToonDNA import ToonDNA
from toontown.toonbase import ToontownGlobals

class DistributedToon(Toon, DistributedSmoothNode, DistributedAvatar):

    def __init__(self, cr):
        Toon.__init__(self)
        DistributedAvatar.__init__(self, cr)
        DistributedSmoothNode.__init__(self, cr)

    def generate(self):
        DistributedSmoothNode.generate(self)
        DistributedSmoothNode.b_setParent(ToontownGlobals.ToonHidden)

    def announceGenerate(self):
        DistributedSmoothNode.announceGenerate(self)
        DistributedSmoothNode.b_setParent(ToontownGlobals.ToonRender)
        
    def setDNAString(self, dnaStr):
        Toon.setDNAString(self, dnastr)

    def disable(self):
        DistributedSmoothNode.disable(self)
        DistributedSmoothNode.b_setParent(ToontownGlobals.ToonHidden)
        
    