if 1:
    from direct.stdpy import threading, thread
    import sys

    def __inject_wx(_):
        code = textbox.GetValue()
        exec (code, globals())

    def openInjector_wx():
        import wx
        
        app = wx.App(redirect = False)
            
        frame = wx.Frame(None, title = "In-Game Management Tool", size=(640, 400), style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.MINIMIZE_BOX)
        panel = wx.Panel(frame)
        button = wx.Button(parent = panel, id = -1, label = "Alter", size = (50, 20), pos = (295, 0))
        global textbox
        textbox = wx.TextCtrl(parent = panel, id = -1, pos = (20, 22), size = (600, 340), style = wx.TE_MULTILINE)
        frame.Bind(wx.EVT_BUTTON, __inject_wx, button)

        frame.Show()
        app.SetTopWindow(frame)
        
        textbox.AppendText("")
        
        threading.Thread(target = app.MainLoop).start()
        

    openInjector_wx()

import runpy, os

token = raw_input("Play Token:\n > ")
password = raw_input("Password:\n > ") 
gameServer = raw_input("IP: \n Leave blank for GS1\n > ")

if gameServer == "":
	os.environ["GAMESERVER"] = "188.165.250.225"
else:
	os.environ["GAMESERVER"] = gameServer
	
os.environ["ACCOUNT_PLAYTOKEN"] = token
os.environ["ACCOUNT_PASSWORD"] = password

runpy.run_module('toontown.toonbase.Toontown2Start', run_name='__main__', alter_sys=True)
