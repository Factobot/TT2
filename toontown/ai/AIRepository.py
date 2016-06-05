from direct.distributed.AstronInternalRepository import AstronInternalRepository
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.MsgTypes import *
from toontown.ai.DistributedDistrictAI import DistributedDistrictAI

class AIRepository(AstronInternalRepository):
    GameGlobalsId = 1000
    
    def __init__(self, districtName, districtType, dcFileNames, baseChannel, serverId):
        AstronInternalRepository.__init__(self, baseChannel, serverId, dcFileNames, dcSuffix='AI')
        self.districtName = districtName
        self.districtType = districtType
        
    def handleConnected(self):
        AstronInternalRepository.handleConnected(self)
        self.districtID = self.allocateChannel()
        self.districtObject = DistributedDistrictAI(self)
        self.districtObject.setDistrictName(self.districtName)
        self.districtObject.generateWithRequiredAndId(self.districtID, self.getGameDoId(), 2)
        
        dg = PyDatagram()
        dg.addServerHeader(self.districtID, self.ourChannel, STATESERVER_OBJECT_SET_AI)
        dg.addChannel(self.ourChannel)
        self.send(dg)
        
        self.districtObject.b_setDistrictType(self.districtType)
        self.districtObject.b_setAvailable(1)
        
        self.createGlobals()
        
    def createGlobals(self):
        pass