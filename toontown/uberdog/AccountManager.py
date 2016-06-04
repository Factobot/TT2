from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal

class AccountManager(DistributedObjectGlobal):

    def __init__(self, cr):
        DistributedObjectGlobal.__init__(self, cr)
    
    def requestLogin(self, token, password):
        self.sendUpdate('requestLogin', [token, password])

    def recieveAvatar(self, avatar):
        avList = [ ]

        if len(avatar) > 0:
            avList.append(avatar)

        messenger.send('loginDone', [avList])