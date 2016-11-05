#Embedded file name: toontown.dna.DNAStorageElement
from DNAElement import DNAElement
from DNAParser import *

class DNAStorageElement(DNAElement):

    def __init__(self):
        DNAElement.__init__(self)
        self.scope = None

    def getScope(self):
        if self.scope is not None:
            return self.scope
        if self.parent is not None:
            return self.parent
        raise DNAParseError('No scope defined')

    def store(self, storage):
        self._store(storage)
        for child in self.children:
            child.store(storage)

    def _store(self, storage):
        pass
