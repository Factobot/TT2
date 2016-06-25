from toontown.city.DistributedLevelAI import DistributedLevelAI

class LevelLoaderAI:

    def __init__(self, air):
        self.air = air
        self.doId2do = { }

    def generateLevel(self, levelZoneId, levelModel, levelLocation):
        level = DistributedLevelAI(self.air, levelZoneId, levelModel, levelLocation)
        level.generateWithRequired(levelZoneId)
        self.addDo2Table(level)

    def addDo2Table(self, do):
        self.doId2do[do.doId] = do