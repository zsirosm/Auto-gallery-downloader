import multiprocessing as mp
import threading
import random
import time


class Listener(threading.Thread):
    def __init__(self, event, pipe, daemonArg = True):
        threading.Thread.__init__(self, daemon=daemonArg)
        self.event = event
        self.connection = getConnObject(pipe, "receiver")
        self.listeners = {}

    def listen(self):    
        self.event.wait()
        print("responding to event in ", mp.current_process().name)
        eventObject = self.connection.recv()
        print("Incoming message: ", eventObject.get("type"))
        self.emitEvent(eventObject)
        self.listen()

    def run(self):
        print("starting to listen for events", mp.current_process().name)
        self.listen()

    def addEventListener(self, eventType, callback):
        newEventListener = {
            "callback": callback,
        }
        listeners = self.listeners.get(eventType)
        if listeners:
            listeners.append(newEventListener)
        else:
            self.listeners[eventType] = [newEventListener]

    def emitEvent(self, event):
        type = event.get("type")
        listeners = self.listeners.get(type, [])
        for listener in listeners:
            print("using listener", listener)
            listener["callback"](event)



class Error(Exception):
    def __init__(self, message):
        self.message = message


def printMessage(message):
    print(message)


def initializeThread(receiver, pipe):
    thread = Listener(receiver, pipe)
    # thread.daemon = True
    thread.start()
    return thread

def getConnObject(pipe, type):
    if type == 'sender':
        return pipe[1]
    elif type == "receiver":
        return pipe[0]
    else:
        raise Error("Incorrect connection object type for pipe. Only sender/receiver is supported.")

class BaseProcess(mp.Process):
    def __init__(self, senderEvent, receiverEvent, pipe):
        mp.Process.__init__(self)

        self.senderEvent = senderEvent
        self.receiverEvent = receiverEvent
        self.pipe = pipe
        self.activeListeners = {
            "setReady": True,
        }

    # IS NOT WORKING!!
    def emitEvent(self, type, eventData):
        print("is thing on?: ", type, self.activeListeners.get(type))
        # if self.activeListeners.get(type):
        senderConn = getConnObject(self.pipe, "sender")
        eventData = { 
            "type": type,
            "event": eventData,
        }
        senderConn.send(eventData)
        self.senderEvent.set()
        self.senderEvent.clear()

    def setActiveListeners(self, event):
        eventData =  event.get("event")
        self.activeListeners.set(eventData.get("eventName"), True)
        print("set listener for: ", eventData.get("eventName"))

    # is basically a constructor
    # what is in the real constructor is still happening on the main process
    def run(self):
        self.eventThread = initializeThread(self.receiverEvent, self.pipe)
        self.eventThread.addEventListener("addeventlistener", self.setActiveListeners)
        self.emitEvent("setReady", {"isReady": True})

        self.runProcess()


    def runProcess(self):
        eventsToSend = random.randint(10, 25)
        self.emitEvent("logging", f"There will be {eventsToSend} events.")
        for index in range(1, eventsToSend + 1):
            time.sleep(random.randint(1,5))
            print("Sending event:")
            self.emitEvent("logging", { "message": f"{index}. Generating number: {random.random()}" } )

        print("Process ending.")



class BaseProcessController():
    def __init__(self, autoStart = True):
        self.receiverEvent = mp.Event()
        self.senderEvent = mp.Event()
        self.pipe = mp.Pipe(True)
        self.eventThread = initializeThread(self.receiverEvent, self.pipe)
        self.process = BaseProcess(self.receiverEvent, self.senderEvent, self.pipe)
        self.isReady = False
        if autoStart:
            self.start()

    def start(self):
        self.process.start()
        self.eventThread.addEventListener("setReady", self.setReady)
        while not self.isReady:
            print("not ready!")
            time.sleep(0.02)


    def addEventListener(self, eventName, callback):
        print("adding listener...")
        eventData = {
            "type": "addeventlistener", 
            "event": { "eventName": eventName },
        }
        self.eventThread.addEventListener(eventName, callback)
        senderConn = getConnObject(self.pipe, "sender")
        senderConn.send(eventData)
        self.senderEvent.set()
        self.senderEvent.clear()

    def getProcess(self):
        return self.process
    
    def setReady(self, event):        
        self.isReady = True
        print("Process is ready!", event)



def printEventMessage(event):
    eventData = event.get("event")
    print("yoooo, message from another process", eventData.get("message"))


def initializeProcess():
    processController = BaseProcessController()
    processController.addEventListener("logging", printEventMessage)



if __name__ == '__main__':
    initializeProcess()
