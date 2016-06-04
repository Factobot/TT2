from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.MsgTypes import *
from time import gmtime, strftime
import base64, os, json, pyaes

class AccountManagerUD(DistributedObjectGlobalUD):
    dbStorageFilename = 'db-storage.json'
    dbStoreStucture = {
        'Accounts': {
        }
    }

    dbId = 4003 # look to the astron config.

    # Encryption:
    encryptionKey = 'TT2.0_DB_STORE_ENCRYPT__' # This will work for now.
    aes = pyaes.AESModeOfOperationCTR(encryptionKey)

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)
        self.playToken2connection = { }
        self.accountId2connection = { }
        self.createStore()

    def createStore(self):
        if not os.path.exists(self.dbStorageFilename):
            with open(self.dbStorageFilename, 'w+') as store:
                json.dump(self.dbStoreStucture, store)
                store.close()

    def generateSeason(self):
        pass

    def encryptValue(self, value):
        return self.aes.encrypt(value)

    def decryptValue(self, value):
        return self.aes.decrypt(value)

    def requestLogin(self, token, password):
        self.token = token

        sender = self.air.getMsgSender()
        self.playToken2connection[token] = sender

        if len(self.token) == 0:
            return

        (ret, data) = self.checkIfStored(self.token)

        if ret == 'success':
            self.updateStoredAccount(self.token)
        else:
            self.createNewAccount(self.token, password)

    def checkIfStored(self, token):
        with open(self.dbStorageFilename, 'rb') as store:
            jdata = json.load(store)
            store.close()
        
        accounts = jdata['Accounts']
        if token in accounts:
            return ('success', accounts[token])

        return ('failure', None)

    def createNewAccount(self, token, password):
        fields = {
            'ACCOUNT_USERNAME': self.encryptValue(token),
            'ACCOUNT_PASSWORD': self.encryptValue(password),
            'ACCOUNT_TIME_CREATED': strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            'ACCOUNT_LAST_LOGIN': strftime("%Y-%m-%d %H:%M:%S", gmtime())
        }

        self.air.dbInterface.createObject(self.dbId, 
                                    dclass=self.air.dclassesByName['AccountManagerUD'], 
                                    fields=fields, 
                                    callback=self._createdAccount)

    def _createdAccount(self, doId): # created account callback.
        self._updateAccountOnCreation(doId)
        self._activateSender(doId)

    def _updateAccountOnCreation(self, doId):
        with open(self.dbStorageFilename, 'r') as store:
            jdata = json.load(store)
            store.close()
            
        jdata['Accounts'][self.token] = str(doId)

        with open(self.dbStorageFilename, 'r+') as store:
            store.write(json.dumps(jdata))

    def updateStoredAccount(self, token):
        with open(self.dbStorageFilename, 'r') as store:
            jdata = json.load(store)
            store.close()

        fields = {
            'ACCOUNT_LAST_LOGIN': strftime("%Y-%m-%d %H:%M:%S", gmtime())
        }

        self.air.dbInterface.updateObject(self.dbId,
                                        doId=jdata['Accounts'][token],
                                        dclass=self.air.dclassesByName['AccountManagerUD'],
                                        newFields=fields,
                                        callback=self._updatedStoredAccount)

    def _updatedStoredAccount(self, doId):
        if doId == None:
            if self.token in self.playToken2connection:
                doId = self.playToken2connection[self.token]
            else:
                return
        
        # TODO: get avatars and send here.
        self._activateSender(doId)

    def _activateSender(self, channel, avatar=None):
        target = self.playToken2connection[self.token]
        self.accountId2connection[channel] = target

        datagram = PyDatagram()
        datagram.addServerHeader(target, self.air.ourChannel, CLIENTAGENT_SET_STATE)
        datagram.addUint16(1) # ANONYMOUS
        self.air.send(datagram)
        datagram.clear() # Cleanse data

        datagram = PyDatagram()
        datagram.addServerHeader(target, self.air.ourChannel, CLIENTAGENT_OPEN_CHANNEL)
        datagram.addUint64(channel) # TODO!
        self.air.send(datagram)
        datagram.clear() # Cleanse data

        datagram = PyDatagram()
        datagram.addServerHeader(target, self.air.ourChannel, CLIENTAGENT_SET_CLIENT_ID)
        datagram.addUint64(channel << 32) # TODO!
        self.air.send(datagram)
        datagram.clear() # Cleanse data

        datagram = PyDatagram()
        datagram.addServerHeader(target, self.air.ourChannel, CLIENTAGENT_SET_STATE)
        datagram.addUint16(2) # ESTABLISHED
        self.air.send(datagram)
        datagram.clear() # Cleanse data

        # We're done here send a response.
        if avatar == None:
            self.sendUpdateToChannel(target, 'recieveAvatar', [])