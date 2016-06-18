from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal

class AvatarManager(DistributedObjectGlobal):
    
    def __init__(self, cr):
        DistributedObjectGlobal.__init__(self, cr)
        
    def createAvatar(self, slot, name, dna):
        self.sendUpdate('requestCreateAvatar', [slot, name, dna.makeNetString()])
        
    def createAvatarResponse(self, avId):
        messenger.send("AvatarManager__AvatarCreationDone", [avId])
        
    def sendChooseAvatar(self, avId):
        self.sendUpdate("chooseAvatar", [avId])