from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from toontown.distributed.PotentialToon import 
import pyotp, string

class AccountManager(DistributedObjectGlobal):

    def __init__(self, cr):
        DistributedObjectGlobal.__init__(self, cr)
        self.__totp = pyotp.TOTP(''.join(random.SystemRandom().choice(string.ascii_uppercase) for _ in range(1024)))
    
    def __generateSecurityKey(self):
        return self.__totp.now()
    
    def requestLogin(self, token, password):
        __key = self.__generateSecurityKey()
        self.sendUpdate('requestLogin', [token, password, __key])

    def recieveAvatar(self, avList):
        avList = list(avList)
        newAvList = []
        for av in avList:
            pot = PotentialToon(avId=av[0], dna=av[1], name=av[2])
            newAvList.append(pot)
            
        messenger.send('loginDone', [newAvList])