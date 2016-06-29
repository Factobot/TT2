from SocketServer import TCPServer, BaseRequestHandler
from direct.directnotify.DirectNotifyGlobal import *
import threading, json

'''
Packet Structure:

  Request Login:
    {'request': ['request-login', 'username', 'hashed_password']}

  Response Login:
    {'request': ['response-login_resp', 'success_status', 'reason_string']}

'''

BUFFERSIZE = 1024
QUEUESIZE = 10000
ALLOWREUSE = True

requestTypes = [
    'request-login',
    'request-login_resp'
    'request-create',
]

class RequestHandler(BaseRequestHandler):
    notify = directNotify.newCategory("RequestHandler")
    notify.setInfo(True)
    notify.setWarning(True)

    def handle(self):
        data = str(self.request.recv(BUFFERSIZE))
        if len(data) == 0:
            return
        
        jdata = json.loads(data)

        try:
            requestType = jdata['type']
        except:
            self.notify.warning('Recieved an invalid requestType!')
            # Invalid requestType recieved!
            return

        if requestType == requestTypes[0]:
            self.requestLogin(jdata['username'], jdata['password'])
        elif requestTypes == requestTypes[1]:
            # TODO: handle account creation...
            self.requestCreate()

    def requestLogin(self, username, password):
        with open('db-storage.json', 'rb') as storage:
            jdata = json.load(storage)
            accounts = jdata['Accounts']
            # We're done close the storage file.
            storage.close()

        if username in accounts:
            response = {
                "type":"response-login_resp", "result":"access-granted", "reason": "Login sucess!", str(username)
            }

            self.sendResponse(json.dumps(response))
            return

        response = {
            "type":"response-login_resp", "result":"access-denied", "reason": "No accounts with that credentials were found in the database, perhapse you mispelled your password or username."
        }

        self.sendResponse(json.dumps(response))
        return

    def requestCreate(self):
        return NotImplemented

    def sendResponse(self, response):
        if len(response) == 0:
            return

        self.request.send(response)

class AccountBackdoor(TCPServer):
    TCPServer.request_queue_size = QUEUESIZE
    TCPServer.allow_reuse_address = ALLOWREUSE
    notify = directNotify.newCategory("AccountBackdoor")
    notify.setInfo(True)

    def __init__(self, host, port):
        TCPServer.__init__(self, (host, port), RequestHandler)
        self.hostDetails = [host, port]

    def startServer(self):
        self.process = threading.Thread(target=self.serve_forever)
        self.process.daemon = True
        self.process.start()
        self.notify.info('Authenication backdoor started on: %s:%d' % (self.hostDetails[0], self.hostDetails[1]))

    def stopServer(self):
        if self.process:
            self.process = None
            del self.process

        self.notify.info('Stopping backdoor, please wait...')
        self.shutdown()
        self.server_close()
