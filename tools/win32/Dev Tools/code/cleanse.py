import os

extensions = ('.pyc','.pyo')
trashFiles = ('parsetab.py',)

print 'Changing to root directory...'
os.chdir('../../../toontown/')

print 'Scanning for garbage files...'


def delete(filepath):
    print "Removing '%s'..." % filepath
    os.unlink(filepath)


for root, folders, files in os.walk('.'):
    for filename in files:
        filepath = os.path.join(root, filename)
        if os.path.splitext(filename)[1] in extensions:
            delete(filepath)
        elif filename in trashFiles:
            delete(filepath)

print 'Done.'
