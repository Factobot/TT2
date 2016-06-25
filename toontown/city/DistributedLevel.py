from direct.distributed.DistributedNode import DistributedNode

class DistributedLevel(DistributedNode):

    def __init__(self, cr):
        DistributedNode.__init__(self, cr)
        self.levelZoneId = 0
        self.levelModel = None
        self.levelLocation = None
        self.environment = None

    def generate(self):
        DistributedNode.generate(self)
        self.cr.levelObject = self

    def announceGenerate(self):
        DistributedNode.announceGenerate(self)

    def setLevelZoneId(self, zoneId):
        self.levelZoneId = zoneId

    def setLevelModel(self, model):
        self.levelModel = model

    def setLevelXYZHPR(self, x, y, z, h, p, r):
        self.levelLocation = [x, y, z, h, p, r]

    def requestEnter(self):
        self.sendUpdate('requestEnter', [
            ])

    def loadLevel(self):
        self.unloadLevel()

        if self.levelModel:
            self.environment = loader.loadModel(self.levelModel)
            self.environment.setPosHpr(*self.levelXYZHPR)
            self.environment.flattenMedium()
            self.environment.wrtReparentTo(render)

        messenger.send('levelCreated')

    def unloadLevel(self):
        if self.environment:
            self.environment.removeNode()

        self.environment = None
