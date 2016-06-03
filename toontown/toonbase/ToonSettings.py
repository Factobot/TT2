import cPickle, base64, hashlib, zlib

DEFAULT_SETTINGS = {
    'display': 'pandagl'
}

class ToonSettings:
    
    def __init__(self):
        self.settings = {}
        self.hashSecret = zlib.compress(base64.b64encode(hashlib.md5('settings_secret').digest()))
        
    def save(self):
        with open('settings.stg', 'wb') as settingsFile:
            dump = cPickle.dumps(self.settings)
            # this is some lame encrypting, i know, its just a placeholder
            dump1 = dump[0:(len(dump)/2)+1] 
            dump2 = dump[(len(dump)/2)+1:len(dump)]
            encode = base64.b64encode(dump2 + self.hashSecret + dump1)
            settingsFile.write(encode)
            settingsFile.close()
    
    def read(self):
        with open('settings.stg', 'rb') as settingsFile:
            contents = settingsFile.read()
            contents = contents.replace(self.hashSecret, '')
            try:
                undecoded = base64.b64decode(contents)
                unpickled = cPickle.loads(undecoded)
                self.settings = unpickled
            except:
                print 'Corrupted settings data! Creating a new one.'
                self.settings = DEFAULT_SETTINGS
                self.save()
            
            settingsFile.close()
            