import runpy, os

token = raw_input("Play Token:\n > ")
password = raw_input("Password:\n > ") 
gameServer = raw_input("IP: \n Leave blank for GS1\n > ")
OTPKey = raw_input("OTPKey: ")

if gameServer == "":
	os.environ["GAMESERVER"] = "188.165.250.225"
else:
	os.environ["GAMESERVER"] = gameServer
	
os.environ["ACCOUNT_PLAYTOKEN"] = token
os.environ["ACCOUNT_PASSWORD"] = password

if OTPKey != "":
	os.environ["OTPKey"] = OTPKey

runpy.run_module('toontown.toonbase.Toontown2ProductionStart', run_name='__main__', alter_sys=True)
