from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.distributed.PyDatagram import *
from direct.distributed.MsgTypes import *
from direct.fsm.FSM import *
from toontown.toon.ToonDNA import ToonDNA
from toontown.login import PickerGlobals

class Operation(FSM):

    def __init__(self, avMgr, accId, slotId, name, dnaString, avId):
        FSM.__init__(self, self.__class__.__name__)
        self.avMgr = avMgr
        self.air = self.avMgr.air
        self.accId = accId
        self.slotId = slotId
        self.name = name
        self.dnaString = dnaString
        self.avId = avId
        
    def connId(self, accId):
        return self.avMgr.GetAccountConnectionChannel(accId)
        
    def enterOff(self):
        del self.avMgr.acc2operation[self.accId]
        
    def enterQueryAccount(self):
        self.air.dbInterface.queryObject(databaseId=self.air.dbId, 
                                            doId=self.accId, 
                                            callback=self.__handleQueryDone)
                                            
    def __handleQueryDone(self, dclass, fields):
        if dclass != self.avMgr.air.dclassesByName['AccountManagerUD']:
            self.killConnection("Unknown account")
            return

        self.accountData = fields
        self.avList = list(self.accountData['ACCOUNT_AVATARS'])
        self.handleQueryDone()
        
    def killConnection(self, reason):
        self.avMgr.dropConnection(self.connId(self.accId), reason)
        self.demand("Off")

class AvatarCreation(Operation):

    def handleQueryDone(self):
        if self.avList[self.slotId] != 0:
            self.killConnection("Attempted to create toon in occupied slot.")
            return

        self.request("CreateToon")
        
    def enterCreateToon(self):
        fields = {
            'setDNAString': (self.dnaString,),
            'setName': (self.name,),
        }

        self.air.dbInterface.createObject(
            self.air.dbId,
            self.air.dclassesByName['DistributedToonUD'],
            fields,
            self.__handleAvatarCreated
        )
        
    def __handleAvatarCreated(self, doId):
        if not doId:
            self.killConnection("Failed to create a new avatar!")
            return

        self.avId = doId
        self.request("Store")
        
    def enterStore(self):
        self.avList[self.slotId] = self.avId
        self.air.dbInterface.updateObject(
            self.air.dbId,
            self.accId,
            self.avMgr.air.dclassesByName['AccountManagerUD'],
            {'ACCOUNT_AVATARS': self.avList},
            {'ACCOUNT_AVATARS': self.accountData["ACCOUNT_AVATARS"]},
            self.__handleStoreDone
        )

    def __handleStoreDone(self, fields):
        self.avMgr.sendUpdateToAccountId(self.accId, 'createAvatarResponse', [self.avId])
        self.demand("Off")
        
class AvatarLoading(Operation):
    
    def handleQueryDone(self):
        if self.avId not in self.avList:
            self.killConnection("Tried to play avatar not in list,")
            return
        
        self.demand("QueryAvatar")
        
    def enterQueryAvatar(self):
        self.air.dbInterface.queryObject(self.air.dbId, self.avId, self.__handleAvatarResp)
        
    def __handleAvatarResp(self, dclass, fields):
        if dclass != self.air.dclassesByName['DistributedToonUD']:
            self.killConnection('Invalid avatar in account.')
            return
        
        self.avatar = fields
        self.demand('SetAvatar')
        
    def enterSetAvatar(self):
        channel = self.avMgr.GetAccountConnectionChannel(self.accId)

        # If they disconnect during the operation, we give a post remove.
        dgcleanup = PyDatagram()
        dgcleanup.addServerHeader(self.avId, channel, STATESERVER_OBJECT_DELETE_RAM)
        dgcleanup.addUint32(self.avId)
        dg = PyDatagram()
        dg.addServerHeader(channel, self.air.ourChannel, CLIENTAGENT_ADD_POST_REMOVE)
        dg.addString(dgcleanup.getMessage())
        self.air.send(dg)

        self.air.sendActivate(
            self.avId, 0, 0)
        
        # Add to the avatar channel
        dg = PyDatagram()
        dg.addServerHeader(channel, self.air.ourChannel, CLIENTAGENT_OPEN_CHANNEL)
        dg.addChannel(self.avMgr.GetPuppetConnectionChannel(self.avId))
        self.air.send(dg)

        # Set sender channel to account too
        dg = PyDatagram()
        dg.addServerHeader(channel, self.air.ourChannel, CLIENTAGENT_SET_CLIENT_ID)
        dg.addChannel(self.accId<<32 | self.avId)
        self.air.send(dg)

        # Get control and finish.
        dg = PyDatagram()
        dg.addServerHeader(self.avId, self.air.ourChannel, STATESERVER_OBJECT_SET_OWNER)
        dg.addChannel(self.accId<<32 | self.avId)
        self.air.send(dg)
        self.demand("Off")


class AvatarManagerUD(FSM, DistributedObjectGlobalUD):

    def __init__(self, air):
        FSM.__init__(self, 'AvatarManager')
        DistributedObjectGlobalUD.__init__(self, air)
        self.acc2operation = {}
        
    def dropConnection(self, connectionId, reason):
        dg = PyDatagram()
        dg.addServerHeader(connectionId, self.air.ourChannel, CLIENTAGENT_EJECT)
        dg.addUint16(122)
        dg.addString(reason)
        self.air.send(dg)
        
    def requestCreateAvatar(self, slotId, name, dna):
        sender = self.air.getMsgSender()
        if slotId > PickerGlobals.NUM_TOONS:
            self.dropConnection(sender, 'Invalid slotId given!')
            return
        
        valid = ToonDNA().isValidNetString(dna)
        if not valid:
            self.dropConnection(sender, "Invalid DNA given!")
            return

        accountId = self.air.getAccountIdFromSender()
        self.acc2operation[accountId] = AvatarCreation(self, accountId, slotId, name, dna, None)
        self.acc2operation[accountId].request('QueryAccount')
        
    def chooseAvatar(self, avId):
        currentAvId = self.air.getAvatarIdFromSender()
        accountId = self.air.getAccountIdFromSender()
        sender = self.air.getMsgSender()
        
        if currentAvId:
            self.dropConnection(sender, 'A Toon is already chosen!')
            return
            
        self.acc2operation[accountId] = AvatarLoading(self, accountId, None, None, None, avId)
        self.acc2operation[accountId].request("QueryAccount")
        