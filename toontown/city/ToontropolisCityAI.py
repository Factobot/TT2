from TestStarter import TestStarter

BlockMap = {
    #block_zoneId:[DistributedObjectStarterX,DistributedObjectStarterY,...]
    #eg: 10101:[TrolleyStarter, FishingStarter]
    10101: [TestStarter]
}

class ToontropolisCityAI:
    def __init__(self, air, zone):
        self.air = air
        self.zone = zone
        self.block2Starters = {}
        
    def start(self):
        for blockZone in BlockMap.keys():
            self.block2Starters[blockZone] = BlockMap[blockZone](self.air, self.zone)
            self.block2Starters[blockZone].start()