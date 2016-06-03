from pandac.PandaModules import *
from direct.fsm.FSM import FSM
from direct.directnotify.DirectNotifyGlobal import *
from direct.distributed.ClientRepositoryBase import ClientRepositoryBase
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.MsgTypes import *
from direct.interval.IntervalGlobal import *
from toontown.login.ToonPicker import ToonPicker

class ToontownClientRepository(ClientRepositoryBase, FSM):
    notify = directNotify.newCategory("ToontownClientRepository")
    notifier = notify # assert notifier
    
    defaultTransitions = {
        'Off': [
            'enterConnect',
            'exitConnect',
            'enterLogin',
            'exitLogin'
        ],
        'enterConnect': [
            'exitConnect',
            'enterNoConnection',
            'enterLogin'
        ],
        'enterLogin': [
            'exitLogin',
            'enterLoginDone'
        ],
        'enterLoginDone': [
            'exitLoginDone'
        ]
    }

    GameGlobalsId = 1000
    DO_ID_ACCOUNT_MANAGER = 1001

    def __init__(self, dcFileNames, serverVersion, serverList, accountDetails):
        ClientRepositoryBase.__init__(self, dcFileNames)
        FSM.__init__(self, 'TCR')
        
        self.serverVersion = serverVersion
        self.serverList = serverList
        self.accountDetails = accountDetails
        self.accountManager = self.generateGlobalObject(self.DO_ID_ACCOUNT_MANAGER, 'AccountManager')

    def getPlayToken(self):
        return str(self.accountDetails[0])

    def getPassword(self):
        return str(self.accountDetails[1])
    
    def _connect(self):
        self.request('Connect')
    
    def enterConnect(self):
        self.url = URLSpec('http://%s:%s' % (self.serverList[0], self.serverList[1]))
        self.connect([self.url], successCallback=self._handleConnected, failureCallback=self._handleNoConnection)
    
    def _handleConnected(self):
        datagram = PyDatagram()
        datagram.addUint16(CLIENT_HELLO)
        datagram.addUint32(self.hashVal)
        datagram.addString(self.serverVersion)
        self.send(datagram)
    
    def _handleConnectedDone(self):
        self.forceTransition('Login')
    
    def exitConnect(self):
        pass
    
    def _handleNoConnection(self, *args):
        self.forceTransition('NoConnection')
    
    def enterNoConnection(self):
        self.notify.warning('Failed to connect to the gameserver!')
    
    def enterLogin(self):
        self.accept('loginDone', self._handleLoginResp)
        self.accountManager.requestLogin(self.getPlayToken(), self.getPassword())
    
    def exitLogin(self):
        pass

    def removeLoadingScreen(self):
        base.loadingScreen.exit()

    def _handleLoginResp(self, avList):
        self.tookPicker = ToonPicker(avList, "ToonPickerDone")
        base.loadingScreen.enablePlay(avList)
        #self.loadingWait = Sequence(
        #    Wait(17.5),
        #    Func(self.removeLoadingScreen),
        #    Func(self._handleLoginDone, avList)
        #).start()

    def _handleLoginDone(self, avList):
        self.forceTransition('LoginDone', avList)

    def enterLoginDone(self, avList):
        self.tookPicker.enter()
        self.accept("ToonPickerDone", self.__handlePickerDone)
        
    def __handlePickerDone(self, av, slot, status):
        if status == 'create':
            self.forceTransition('CreateToon', slot)
            return

    def exitLoginDone(self):
        pass
        
    def enterCreateToon(self, slot):
        pass
        
    def exitCreateToon(self):
        pass
    
    def handleDatagram(self, di):
        self.handleMessageType(di, self.getMsgType())
    
    def handleMessageType(self, di, msgType):
        if msgType == CLIENT_HELLO_RESP:
            self._handleConnectedDone()
        elif msgType == CLIENT_EJECT:
            self.handleGoGetLost(di)
        elif msgType == CLIENT_HEARTBEAT:
            self.handleServerHeartbeat(di)
        elif msgType == CLIENT_OBJECT_SET_FIELD:
            self.handleUpdateField(di)
        elif msgType == CLIENT_OBJECT_LEAVING:
            pass
        elif msgType == CLIENT_OBJECT_LEAVING_OWNER:
            pass
        elif msgType == CLIENT_ENTER_OBJECT_REQUIRED:
            self.handleGenerateWithRequired(di)
        elif msgType == CLIENT_ENTER_OBJECT_REQUIRED_OTHER:
            self.handleGenerateWithRequired(di, other=True)
        elif msgType == CLIENT_ENTER_OBJECT_REQUIRED_OTHER_OWNER:
            self.handleGenerateWithRequiredOtherOwner(di)
        elif msgType == CLIENT_DONE_INTEREST_RESP:
            self.gotInterestDoneMessage(di)
        elif msgType == CLIENT_OBJECT_LOCATION:
            self.gotObjectLocationMessage(di)
        else:
            self.notify.warning('Recieved an unexpected msgType: %d' % (msgType))
            return None
        
    def handleGenerateWithRequired(self, di, other=False):
        doId = di.getUint32()
        parentId = di.getUint32()
        zoneId = di.getUint32()
        classId = di.getUint16()

        dclass = self.dclassesByNumber[classId]
        if self._isInvalidPlayerAvatarGenerate(doId, dclass, parentId, zoneId):
            return None
        
        dclass.startGenerate()
        distObj = self.generateWithRequiredFields(dclass, doId, di, parentId, zoneId)
        dclass.stopGenerate()

    def handleGenerateWithRequiredOtherOwner(self, di):
        doId = di.getUint32()
        parentId = di.getUint32()
        zoneId = di.getUint32()
        classId = di.getUint16()
        
        dclass = self.dclassesByNumber[classId]
        dclass.startGenerate()
        distObj = self.generateWithRequiredOtherFieldsOwner(dclass, doId, di)
        dclass.stopGenerate()

    def gotInterestDoneMessage(self, di):
        if self.deferredGenerates:
            dg = Datagram(di.getDatagram())
            di = DatagramIterator(dg, di.getCurrentIndex())
            self.deferredGenerates.append((CLIENT_DONE_INTEREST_RESP, (dg, di)))
        else:
            self.handleInterestDoneMessage(di)

    def gotObjectLocationMessage(self, di):
        if self.deferredGenerates:
            dg = Datagram(di.getDatagram())
            di = DatagramIterator(dg, di.getCurrentIndex())
            di2 = DatagramIterator(dg, di.getCurrentIndex())
            doId = di2.getUint32()
            if doId in self.deferredDoIds:
                self.deferredDoIds[doId][3].append((CLIENT_OBJECT_LOCATION, (dg, di)))
            else:
                self.handleObjectLocation(di)
        else:
            self.handleObjectLocation(di)
            

            
            
            