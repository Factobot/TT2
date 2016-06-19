from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from toontown.distributed.PotentialToon import *

class AccountManager(DistributedObjectGlobal):

    def __init__(self, cr):
        DistributedObjectGlobal.__init__(self, cr)
    
    def requestLogin(self, token, password):
        self.sendUpdate('requestLogin', [token, password])

    def recieveAvatar(self, avList):
        avList = list(avList)
        newAvList = []
        for av in avList:
            pot = PotentialToon(dna=av[0], name=av[1], slot=av[2])
            newAvList.append(pot)
            
        messenger.send('loginDone', [newAvList])