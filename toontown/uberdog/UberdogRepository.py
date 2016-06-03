from direct.distributed.AstronInternalRepository import AstronInternalRepository
from direct.distributed.PyDatagram import *

class UberdogRepository(AstronInternalRepository):
    DO_ID_ACCOUNT_MANAGER = 1001

    def __init__(self, dcFileNames, baseChannel, serverId):
        AstronInternalRepository.__init__(self, baseChannel, serverId, dcFileNames, dcSuffix='UD')
        
    def getAvatarIdFromSender(self):
        return self.getMsgSender() & 0xFFFFFFFF

    def getAccountIdFromSender(self):
        return (self.getMsgSender() >> 32) & 0xFFFFFFFF

    def handleConnected(self):
        AstronInternalRepository.handleConnected(self)
        self.generateGlobals()
    
    def generateGlobals(self):
        self.accountManager = self.generateGlobalObject(self.DO_ID_ACCOUNT_MANAGER, 'AccountManager')