import logging

class CustomHandler(logging.Handler):
    def emit(self, logRecord):
        print("LOG EVENT: ", logRecord)

def registerLogger(name):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    handler = CustomHandler()
    handler.setLevel(logging.DEBUG)
    log.addHandler(handler)