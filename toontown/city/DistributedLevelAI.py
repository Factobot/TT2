from direct.distributed.DistributedNodeAI import DistributedNodeAI

class DistributedLevelAI(DistributedNodeAI):

    def __init__(self, air, levelZoneId, levelModel, levelLocation):
        DistributedNodeAI.__init__(self, air)
        self.levelZoneId = levelZoneId
        self.levelModel = levelModel
        self.levelLocation = levelLocation

    def getLevelZoneId(self):
        return self.levelZoneId

    def getLevelModel(self):
        return self.levelModel

    def getLevelLocation(self):
        return self.levelLocation

    def requestEnter(self):
        avatarId = self.air.getAvatarIdFromSender()

        if avatarId not in self.air.doId2do:
            return

        self.sendUpdateToAvatarId(avatarId, 'loadLevel', [
            ])