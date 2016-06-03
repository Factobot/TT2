from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD

class AccountManagerUD(DistributedObjectGlobalUD):

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)

    def requestLogin(self, token):
        pass