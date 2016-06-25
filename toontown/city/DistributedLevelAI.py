from direct.distributed.DistributedNodeAI import DistributedNodeAI

class DistributedLevelAI(DistributedNodeAI):

    def __init__(self, air, levelZoneId, levelModel, levelXYZHPR):
        DistributedNodeAI.__init__(self, air)
        self.levelZoneId = levelZoneId
        self.levelModel = levelModel
        self.levelXYZHPR = levelXYZHPR

    def getLevelZoneId(self):
        return self.levelZoneId

    def getLevelModel(self):
        return self.levelModel

    def getLevelXYZHPR(self):
        return self.levelXYZHPR

    def requestEnter(self):
        self.sendUpdateToAvatarId(self.air.getAvatarIdFromSender(), 'loadLevel', [
            ])
