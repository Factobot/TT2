from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.MsgTypes import *
from time import gmtime, strftime
import base64, os, json

class AccountManagerUD(DistributedObjectGlobalUD):
    dbStorageFilename = 'db-storage.json'
    dbStoreStucture = {
        'Accounts': {
        }
    }

    dbId = 4003 # look to the astron config.

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
            'ACCOUNT_AVATARS': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'ACCOUNT_USERNAME': token,
            'ACCOUNT_PASSWORD': password,
            'ACCOUNT_TIME_CREATED': strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            'ACCOUNT_LAST_LOGIN': strftime("%Y-%m-%d %H:%M:%S", gmtime())
        }

        self.air.dbInterface.createObject(self.dbId, 
                                    dclass=self.air.dclassesByName['AccountManagerUD'], 
                                    fields=fields, 
                                    callback=self._createdAccount)

    def _createdAccount(self, doId): # created account callback.
        self._updateAccountOnCreation(doId)
        self._activateSender(doId, avatar=[])

    def _updateAccountOnCreation(self, doId):
        with open(self.dbStorageFilename, 'r') as store:
            jdata = json.load(store)
            store.close()
        
        newData = jdata
        newData['Accounts'][self.token] = doId

        with open(self.dbStorageFilename, 'r+') as store:
            store.write(json.dumps(newData))

    def updateStoredAccount(self, token):
        with open(self.dbStorageFilename, 'r') as store:
            jdata = json.load(store)
            store.close()

        doId = int(jdata['Accounts'][token])
        fields = {
            'ACCOUNT_LAST_LOGIN': strftime("%Y-%m-%d %H:%M:%S", gmtime())
        }

        self.air.dbInterface.updateObject(databaseId=self.dbId,
                                        doId=doId,
                                        dclass=self.air.dclassesByName['AccountManagerUD'],
                                        newFields=fields,
                                        callback=self._updatedStoredAccount)

    def _updatedStoredAccount(self, doId):
        if doId == None:
            with open(self.dbStorageFilename, 'r') as store:
                jdata = json.load(store)
                store.close()

        self.air.dbInterface.queryObject(self.dbId,
                            doId=jdata['Accounts'][self.token],
                            callback=self._checkForAvatars)

    def _checkForAvatars(self, doId, fields):
        avatarList = fields['ACCOUNT_AVATARS']

        if len(avatarList) > 0:
            for av in avatarList:
                if av != 0:
                    self._activateSender(self.playToken2connection[self.token], avatar=av) # TODO!
        else:
            self._activateSender(self.playToken2connection[self.token], avatar=[])

    def _activateSender(self, channel, avatar):
        target = self.playToken2connection[self.token]
        self.accountId2connection[channel] = target

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
        self.sendUpdateToChannel(target, 'recieveAvatar', [avatar])