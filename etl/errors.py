
class InvalidFilePath(Exception):
    pass

class InvalidInputData(Exception):
    pass

class InvalidAttributeManifest(InvalidInputData):
    pass

class PathExists(Exception):
    pass