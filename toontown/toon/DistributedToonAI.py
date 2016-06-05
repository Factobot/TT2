from direct.distributed.DistributedSmoothNodeAI import DistributedSmoothNodeAI
from toontown.avatar.DistributedAvatarAI import DistributedAvatarAI

class DistributedToonAI(DistributedAvatarAI, DistributedSmoothNodeAI):

    def __init__(self, air):
        DistributedAvatarAI.__init__(self, air)
        DistributedSmoothNodeAI.__init__(self, air)
        self.dnaString = ''
        self.animState = ''
        
    def b_setDNAString(self, dnaStr):
        self.setDNAString(dnaStr)
        self.d_setDNAString(dnaStr)
        
    def d_setDNAString(self, dnaStr):
        self.sendUpdate("setDNAString", [dnaStr])
        
    def setDNAString(self, dnaStr):
        self.dnaString = dnaStr
        
    def getDNAString(self, dnaStr):
        return self.dnaString
        
    def setAnimState(self, animState):
        self.animState = animState
        
    def getAnimState(self, animState):
        return self.animState