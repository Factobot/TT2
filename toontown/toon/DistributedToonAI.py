from direct.distributed.DistributedSmoothNodeAI import *
from toontown.avatar.DistributedAvatarAI import *

class DistributedToonAI(DistributedAvatarAI, DistributedSmoothNodeAI):
    def __init__(self, air):
        DistributedAvatarAI.__init__(self, air)
        DistributedSmoothNodeAI.__init__(self, air)
        self.dnaString = ''
        
    def b_setDNAString(self, dnaStr):
        self.setDNAString(dnaStr)
        self.d_setDNAString(dnaStr)
        
    def d_setDNAString(self, dnaStr):
        self.sendUpdate("setDNAString", [dnaStr])
        
    def setDNAString(self, dnaStr):
        self.dnaString = dnaStr
        
    def getDNAString(self, dnaStr):
        return self.dnaString