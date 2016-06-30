from direct.distributed.AstronInternalRepository import AstronInternalRepository
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.PyDatagram import *
from toontown.distributed import GameGlobals
from toontown.uberdog.SecurityKeyUD import SecurityKeyUD
from toontown.uberdog.Account2Auth import Account2Auth
from toontown.uberdog.AdminServiceUD import AdminServiceUD

class UberdogRepository(AstronInternalRepository):
    GameGlobalsId = GameGlobals.GameGlobalsId
    dbId = 4003
    securityKeyEnabled = 0
    adminServiceEnabled = 0
    
    def __init__(self, dcFileNames, baseChannel, serverId):
        AstronInternalRepository.__init__(self, baseChannel, serverId, dcFileNames, dcSuffix='UD')
        self.securityKey = SecurityKeyUD(self)
        
    def getAvatarIdFromSender(self):
        return self.getMsgSender() & 0xFFFFFFFF

    def getAccountIdFromSender(self):
        return (self.getMsgSender() >> 32) & 0xFFFFFFFF

    def handleConnected(self):
        AstronInternalRepository.handleConnected(self)
        self.securityKey.enable()
        self.createAdminCaC()
        self.createBackdoors()
        self.generateRoot()
        self.generateGlobals()

    def createAdminCaC(self):
        self.AdminServiceUD = AdminServiceUD('127.0.0.1', 6200)
        self.AdminServiceUD.startServer()
    
    def createBackdoors(self):
        self.Account2Auth = Account2Auth('127.0.0.1', 6000)
        self.Account2Auth.startServer()

    def generateRoot(self):
        self.rootObject = DistributedObjectAI(self)
        self.rootObject.generateWithRequiredAndId(self.getGameDoId(), GameGlobals.GameGlobalsId, 0)
    
    def generateGlobals(self):
        self.accountManager = self.generateGlobalObject(GameGlobals.DO_ID_ACCOUNT_MANAGER, 'AccountManager')
        self.avatarManager = self.generateGlobalObject(GameGlobals.DO_ID_AVATAR_MANAGER, 'AvatarManager')
