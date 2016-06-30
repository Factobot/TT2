from SocketServer import TCPServer, BaseRequestHandler
from direct.directnotify.DirectNotifyGlobal import *
import threading, json
import pyotp
import pyaes

'''


                                Warning
                     Packets are not yet encrypted. 
                  Do not use this build in production.



Example Packet Structure:

  Request Login:
    {"type":"request-command", "command":"closeLogin", "token":"Pre-Verified-Token", "key":"000000"}

  Response Login:
    {"type":"response-login_resp", "result":"access-denied", "reason": "No accounts with that credentials were found in the database, perhapse you mispelled your username."}

'''

BUFFERSIZE = 1024
QUEUESIZE = 10000
ALLOWREUSE = True



requestTypes = [
    'request-command', # 0
    'request-invalid', # 1
    'request-heartbeat' # 2
]

#Start of variable registration
   
allowingConnections = True

#End of variable registration


class AdminRequestHandler(BaseRequestHandler):
    notify = directNotify.newCategory("AdminRequestHandler")
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
            response = {
                "type":"response-invalid", "result":"invalid-request", "reason":"The request type provided was invalid, or your structure is invalid."
            }
            self.sendResponse(json.dumps(response))
            return

        if requestType == requestTypes[0]:
            self.verifyCommand(jdata['command'], jdata['token'], jdata['key'])

    def verifyCommand(self, command, token, key):
        return NotImplementedError

    def sendResponse(self, response):
        if len(response) == 0:
            return

        self.request.send(response)

class AdminServiceUD(TCPServer):
    TCPServer.request_queue_size = QUEUESIZE
    TCPServer.allow_reuse_address = ALLOWREUSE
    notify = directNotify.newCategory("AdminServerUD")
    notify.setInfo(True)

    def __init__(self, host, port):
        TCPServer.__init__(self, (host, port), AdminRequestHandler)
        self.hostDetails = [host, port]

    def startServer(self):
        self.process = threading.Thread(target=self.serve_forever)
        self.process.daemon = True
        self.process.start()
        self.notify.info('Admin Command Service started on: %s:%d' % (self.hostDetails[0], self.hostDetails[1]))

    def stopServer(self):
        if self.process:
            self.process = None
            del self.process

        self.notify.info('Stopping Service, please wait...')
        self.shutdown()
        self.server_close()

    def canLogin():
        if allowingConnections:
            return True
        else:
            return False