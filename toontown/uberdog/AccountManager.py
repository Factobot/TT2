from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal

class AccountManager(DistributedObjectGlobal):

    def __init__(self, cr):
        DistributedObjectGlobal.__init__(self, cr)
    
    def requestLogin(self, token, password):
        self.sendUpdate('requestLogin', [token, password])
        # TEMPORARY: THIS ISN'T SUPPOSE TO BE HERE AT ALL!
        #self.recieveAvatar()

    def recieveAvatar(self): # TODO: avatar
        avList = [ ]
        # TODO: unpack recieved values, then pack them by slotId.

        messenger.send('loginDone', [avList])