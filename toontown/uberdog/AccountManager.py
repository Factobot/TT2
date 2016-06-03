from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal

class AccountManager(DistributedObjectGlobal):

    def __init__(self, cr):
        DistributedObjectGlobal.__init__(self, cr)
    
    def requestLogin(self, token):
        self.token = token

        if len(self.token) == 0:
            self.token = 'developer'
        
        self.sendUpdate('requestLogin', [token])
        # TEMPORARY: THIS ISN'T SUPPOSE TO BE HERE AT ALL!
        self.recieveAvatar()

    def recieveAvatar(self): # TODO: avatar
        avList = [ ]
        # TODO: unpack recieved values, then pack them by slotId.

        self.cr._handleLoginResp(avList)