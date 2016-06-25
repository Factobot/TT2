from direct.distributed.AstronInternalRepository import AstronInternalRepository
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.MsgTypes import *
from toontown.ai.DistributedDistrictAI import DistributedDistrictAI
from toontown.toonbase import ToontownGlobals
from toontown.city.LevelLoaderAI import LevelLoaderAI

class AIRepository(AstronInternalRepository):
    GameGlobalsId = 1000
    
    def __init__(self, districtName, districtType, dcFileNames, baseChannel, serverId):
        AstronInternalRepository.__init__(self, baseChannel, serverId, dcFileNames, dcSuffix='AI')
        self.districtName = districtName
        self.districtType = districtType
        self.cityHandles = {}

    def getAvatarIdFromSender(self):
        return self.getMsgSender() & 0xFFFFFFFF

    def getAccountIdFromSender(self):
        return (self.getMsgSender() >> 32) & 0xFFFFFFFF
        
    def handleConnected(self):
        AstronInternalRepository.handleConnected(self)
        self.districtId = self.allocateChannel()
        self.districtObject = DistributedDistrictAI(self)
        self.districtObject.setDistrictName(self.districtName)
        self.districtObject.generateWithRequiredAndId(self.districtId, self.getGameDoId(), 2)
        
        dg = PyDatagram()
        dg.addServerHeader(self.districtId, self.ourChannel, STATESERVER_OBJECT_SET_AI)
        dg.addChannel(self.ourChannel)
        self.send(dg)
        
        self.districtObject.b_setDistrictType(self.districtType)
        self.districtObject.b_setAvailable(1)
        
        self.createGlobals()
        self.createZones()
        
    def createGlobals(self):
        self.levelLoader = LevelLoaderAI(self)
        
    def createZones(self):
        for cityZone in ToontownGlobals.ToontownZones.keys():
            self.levelLoader.generateLevel(cityZone, ToontownGlobals.zone2Details[cityZone][0], ToontownGlobals.zone2Details[cityZone][1])
    
        
