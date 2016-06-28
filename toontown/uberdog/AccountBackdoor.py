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
        data = self.request.recv(BUFFERSIZE)
        if len(data) == 0:
            return

        jdata = json.loads(data)

        try:
            request = jdata['request']
        except:
            self.notify.warning('Recieved an invalid request!')
            # Invalid header recieved.
            return

        requestType = request[0]
        if requestType not in requestTypes:
            self.notify.warning('Recieved an invalid requestType with request: %s!' % str(request))
            # Invalid request type.
            return

        if requestType == requestTypes[0]:
            self.requestLogin(requestType, request[1], request[2])
        elif requestTypes == requestTypes[1]:
            # TODO: handle account creation...
            self.requestCreate()

    def requestLogin(self, username, password):
        with open('db-storage', 'rb') as storage:
            jdata = json.load(storage)
            accounts = jdata['Accounts']
            # We're done close the storage file.
            storage.close()

        if username in accounts:
            response = {
                'response': ['response-login_resp', 'access-granted', 'Success, logging you in!']
            }

            self.sendResponse(json.dumps(response))
            return

        response = {
            'response': ['response-login_resp', 'access-denied', 'No accounts with that credentials were found in the database, perhapse you mispelled your password or username.']
        }

        self.sendResponse(json.dumps(response))

    def requestCreate(self):
        return NotImplemented

    def sendResponse(self, response):
        if len(response) == 0:
            return

        self.request.send(response)

class AccountBackdoor(TCPServer):
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
