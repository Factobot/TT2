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
            for startM in BlockMap[blockZone]:
                if not self.block2Starters.has_key(blockZone):
                    self.block2Starters[blockZone] = []
                st = startM(self.air, self.zone)
                st.start()
                self.block2Starters[blockZone].append(st)