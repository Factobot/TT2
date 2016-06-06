from direct.distributed.DistributedObjectUD import DistributedObjectUD

class DistributedToonUD(DistributedObjectUD):
    def __init__(self, air):
        DistributedObjectUD.__init__(self, air)
        
    def setDNAString(self, dnaStr):
        pass