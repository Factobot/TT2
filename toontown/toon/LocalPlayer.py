from toontown.toon.DistributedToon import *
from toontown.toon.PlayAssistant import *
from toontown.toonbase import ToontownGlobals
from toontown.city import TTPCity

City2Loader = {
    ToontownGlobals.TOONTROPOLIS_ZONE: TTPCity.TTPCity
}

class LocalPlayer(DistributedToon):
    def __init__(self, cr):
        DistributedToon.__init__(self, cr)
        self.playAssistant = PlayAssistant(self)
        self.currentCity = None
        
    def setLocation(self, shardId, zoneId):
        DistributedToon.setLocation(self, shardId, zoneId)
        if zoneId in ToontownGlobals.ToontownZones.keys():
            if zoneId % 100:
                # Zone is a city
                cityLoader = City2Loader[zoneId](zoneId)
                cityLoader.load()
                self.currentCity = cityLoader
        
    def announceGenerate(self):
        DistributedToon.announceGenerate(self)
        self.playAssistant.setup()