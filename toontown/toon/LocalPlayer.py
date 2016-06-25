from toontown.toon.DistributedToon import *
from toontown.toon.PlayAssistant import *
from toontown.toonbase import ToontownGlobals

class LocalPlayer(DistributedToon):
    def __init__(self, cr):
        DistributedToon.__init__(self, cr)
        base.playAssistant = self.playAssistant = PlayAssistant(self)
        self.currentCity = None
        
    def setLocation(self, shardId, zoneId):
        DistributedToon.setLocation(self, shardId, zoneId)
        
    def announceGenerate(self):
        DistributedToon.announceGenerate(self)
        self.playAssistant.setup()