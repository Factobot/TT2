from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
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

        if len(self.token) == 0:
            return

        (ret, data) = self.checkIfStored(self.token)

        if ret == 'success':
            pass
        else:
            self.createNewAccount(self.token, password)

    def checkIfStored(self, token):
        with open(self.dbStorageFilename, 'rb') as store:
            jdata = json.load(store)
            store.close()
        
        accounts = jdata['Accounts']
        if token in accounts:
            return ('success', accounts[token])

        return ('failure', [])

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
        self._updateAccount(doId)

    def _updateAccount(self, doId):
        with open(self.dbStorageFilename, 'r') as store:
            jdata = json.load(store)
            store.close()
            
        jdata['Accounts'][str(self.token)] = str(doId)

        with open(self.dbStorageFilename, 'r+') as store:
            store.write(json.dumps(jdata))