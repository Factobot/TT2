from direct.distributed.DistributedObject import DistributedObject

class TestStarter:
    def __init__(self, air, zoneId):
        self.air = air
        self.zoneId = zoneId
        
    def start(self):
        self.testObject = DistributedObject(self.air)
        self.testObject.generateWithRequired(self.zoneId)