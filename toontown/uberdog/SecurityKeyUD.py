import pyotp, string, random

class SecurityKeyUD:
    def __init__(self, air):
        self.air = air
        self.__currentToken = None
        
    def enable(self):
        self.__totp = pyotp.TOTP(''.join(random.SystemRandom().choice(string.ascii_uppercase) for _ in range(1024)))
        taskMgr.add(self.__updateToken, "UpdateSecurityTokenTask")
        
    def __updateToken(self, task):
        __new = self.__totp.now()
        if self.__currentToken != __new:
            self.__currentToken = __new
        return task.again
        
    def match(self, key):
        return key == self.__currentToken