from direct.stdpy import threading
from libpandadna import DNALoader, DNADoor

class DNABulkLoader(object):
    
    def __init__(self, storage, files):
        super(DNABulkLoader, self).__init__()
        
        self.dnaStorage = storage
        self.dnaFiles = files

    def loadDNAFiles(self):
        for file in self.dnaFiles:
            print 'Reading DNA file...', file
            loadDNABulk(self.dnaStorage, file)
        
        del self.dnaStorage
        del self.dnaFiles

def loadDNABulk(dnaStorage, file):
    dnaLoader = DNALoader()
    dnaLoader.loadDNAFile(dnaStorage, '/%s' % file)

def loadDNAFile(dnaStorage, file):
    print 'Reading DNA file...', file
    dnaLoader = DNALoader()
    node = dnaLoader.loadDNAFile(dnaStorage, '/%s' % file)
    
    if node.node().getNumChildren() > 0:
        return node.node()

def loadDNAFileAI(dnaStorage, file):
    dnaLoader = DNALoader()
    return dnaLoader.loadDNAFileAI(dnaStorage, '/%s' % file)

def setupDoor(a, b, c, d, e, f):
    try:
        e = int(str(e).split('_')[0])
    except:
        print 'setupDoor: error parsing', e
        e = 9999

    DNADoor.setupDoor(a, b, c, d, e, f)
