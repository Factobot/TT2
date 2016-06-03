from direct.distributed.DistributedSmoothNode import *
from toontown.avatar.DistributedAvatar import *
from toontown.toon.Toon import *
from toontown.toon.ToonDNA import *

class DistributedToon(DistributedAvatar, DistributedSmoothNode, Toon):
    def __init__(self, cr):
        Toon.__init__(self)
        DistributedAvatar.__init__(self, cr)
        DistributedSmoothNode.__init__(self, cr)
        
    def setDNAString(self, dnaStr):
        Toon.setDNAString(self, dnastr)
        
    