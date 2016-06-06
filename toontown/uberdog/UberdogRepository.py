from direct.distributed.AstronInternalRepository import AstronInternalRepository
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.PyDatagram import *
from toontown.distributed import GameGlobals

class UberdogRepository(AstronInternalRepository):
    GameGlobalsId = GameGlobals.GameGlobalsId
    
    def __init__(self, dcFileNames, baseChannel, serverId):
        AstronInternalRepository.__init__(self, baseChannel, serverId, dcFileNames, dcSuffix='UD')
        
    def getAvatarIdFromSender(self):
        return self.getMsgSender() & 0xFFFFFFFF

    def getAccountIdFromSender(self):
        return (self.getMsgSender() >> 32) & 0xFFFFFFFF

    def handleConnected(self):
        AstronInternalRepository.handleConnected(self)
        self.generateRoot()
        self.generateGlobals()

    def generateRoot(self):
        self.rootObject = DistributedObjectAI(self)
        self.rootObject.generateWithRequiredAndId(self.getGameDoId(), self.GameGlobalsId, 0)
    
    def generateGlobals(self):
        self.accountManager = self.generateGlobalObject(GameGlobals.DO_ID_ACCOUNT_MANAGER, 'AccountManager')
        self.avatarManager = self.generateGlobalObject(GameGlobals.DO_ID_AVATAR_MANAGER, 'AvatarManager')