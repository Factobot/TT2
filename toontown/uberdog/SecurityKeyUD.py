import pyotp, string, random

class SecurityKeyUD:
    def __init__(self, air):
        self.air = air
        
    def enable(self):
        self.__totp = pyotp.TOTP("DEMOSECRET")
        
    def match(self, key):
        print key, self.__totp.now()
		return str(key)
