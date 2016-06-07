from direct.distributed.DistributedObjectAI import DistributedObjectAI

class TestStarter:
    def __init__(self, air, zoneId):
        self.air = air
        self.zoneId = zoneId
        
    def start(self):
        self.testObject = DistributedObjectAI(self.air)
        self.testObject.generateWithRequired(self.zoneId)