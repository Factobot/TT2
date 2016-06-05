from direct.distributed.DistributedObjectAI import DistributedObjectAI
import DistrictGlobals

class DistributedDistrictAI(DistributedObjectAI):
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.districtName = 'Unset'
        self.districtType = DistrictGlobals.DISTRICT_NONE
        self.available = 0
        
    def setDistrictName(self, name):
        self.districtName = name
        
    def d_setDistrictName(self, name):
        self.sendUpdate("setDistrictName", [name])
        
    def getDistrictName(self):
        return self.districtName
        
    def setDistrictType(self, dType):
        self.districtType = dType
        
    def d_setDistrictType(self, dType):
        self.sendUpdate("setDistrictType", [dType])
        
    def b_setDistrictType(self, dType):
        self.setDistrictType(dType)
        self.d_setDistrictType(dType)
        
    def getDistrictType(self):
        return self.districtType
        
    def setAvailable(self, flag):
        self.available = flag
        
    def d_setAvailable(self, flag):
        self.sendUpdate("setAvailable", [flag])
        
    def b_setAvailable(self, flag):
        self.setAvailable(flag)
        self.d_setAvailable(flag)
        
    def getAvailable(self):
        return self.available
        
        
        