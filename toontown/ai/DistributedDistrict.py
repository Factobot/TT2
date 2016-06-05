from direct.distributed.DistributedObject import DistributedObject
import DistrictGlobals

class DistributedDistrict(DistributedObject):
    neverDisable = 1

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.districtName = 'Unset'
        self.districtType = DistrictGlobals.DISTRICT_NONE
        self.available = 0
        
    def announceGenerate(self):
        DistributedObject.announceGenerate(self)

        if self.districtType == DistrictGlobals.DISTRICT_PUBLIC:
            messenger.send('shardInterestComplete', [self.getDoId(), self.districtName, self.districtType, self.available])

    def setDistrictName(self, name):
        self.districtName = name
        
    def setDistrictType(self, dType):
        self.districtType = dType
        
    def setAvailable(self, flag):
        self.available = flag