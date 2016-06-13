from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.distributed.PyDatagram import *
from direct.distributed.MsgTypes import *
from direct.fsm.FSM import *
from toontown.toon.ToonDNA import ToonDNA
from toontown.login import PickerGlobals

class AvatarCreation(FSM):

    defaultTransitions = {
        'enterQueryAccount': [ 
            'enterCreate'
        ],
        'enterCreate': [ 
            'enterStore'
        ],
        'enterStore': [ 
        ]
    }

    def __init__(self, avMgr, accId, slotId, name, dnaString):
        FSM.__init__(self, 'AvatarCreation')
        
        self.avMgr = avMgr
        self.accId = accId
        self.slotId = slotId
        self.name = name
        self.dnaString = dnaString
        
    def enterQueryAccount(self):
        self.avMgr.air.dbInterface.queryObject(databaseId=self.avMgr.air.dbId, 
                                            doId=self.accId, 
                                            callback=self.__handleQueryDone)
    
    def connId(self, accId):
        return self.avMgr.GetAccountConnectionChannel(accId)
    
    def __handleQueryDone(self, dclass, fields):
        print '__handleQueryDone', dclass, fields

        if dclass != self.avMgr.air.dclassesByName['AccountManagerUD']:
            self.avMgr.dropConnection(self.connId(self.accId), "Unknown account")
            return

        self.accountData = fields
        self.avList = self.accountData['ACCOUNT_AVATARS']

        if self.avList[self.slotId]:
            self.avMgr.dropConnection(self.connId(self.accId), "Slot taken!")
            return

        self.request("Create")
        
    def enterCreate(self):
        fields = {
            'setDNAString': (self.dnaString,),
            'setName': (self.name,),
            'setSlotId': (self.slotId,)
        }

        self.avMgr.air.dbInterface.createObject(
            self.avMgr.air.dbId,
            self.avMgr.air.dclassesByName['DistributedToonUD'],
            fields,
            self.__handleAvatarCreated
        )
        
    def __handleAvatarCreated(self, doId):
        if not doId:
            self.avMgr.dropConnection(self.connId(self.accId), "Failed creating avatar!")
            return

        self.avId = doId
        self.request("Store")
        
    def enterStore(self):
        self.avList[self.slot] = self.avId
        self.avMgr.air.dbInterface.updateObject(
            self.avMgr.air.dbId,
            self.accId,
            self.avMgr.air.dclassesByName['AccountManagerUD'],
            {'ACCOUNT_AVATARS': self.avList},
            {'ACCOUNT_AVATARS': self.accountData['ACCOUNT_AVATARS']},
            self.__handleStoreDone
        )
        
    def __handleStoreDone(self, fields):
        if fields:
            self.avMgr.dropConnection(self.connId(self.accId), "Failed associating avatar!")
            return

        self.avMgr.sendUpdateToAccountId(self.accId, 'createAvatarResponse', [self.avId])


class AvatarManagerUD(FSM, DistributedObjectGlobalUD):

    def __init__(self, air):
        FSM.__init__(self, 'AvatarManager')
        DistributedObjectGlobalUD.__init__(self, air)
        
    def dropConnection(self, connectionId, reason):
        dg = PyDatagram()
        dg.addServerHeader(connectionId, self.air.ourChannel, CLIENTAGENT_EJECT)
        dg.addUint16(122)
        dg.addString(reason)
        self.air.send(dg)
        
    def requestCreateAvatar(self, slot, name, dna):
        sender = self.air.getAvatarIdFromSender()
        if slot > PickerGlobals.NUM_TOONS:
            self.dropConnection(sender, 'Invalid slot given!')
            return
        
        valid = ToonDNA().isValidNetString(dna)
        if not valid:
            self.dropConnection(sender, "Invalid DNA given!")
            return

        accountId = self.air.getAccountIdFromSender()
        fsm = AvatarCreation(self, accountId, slot, name, dna)
        fsm.request('QueryAccount')
        
        
        
        
        