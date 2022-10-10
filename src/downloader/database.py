from rethinkdb import RethinkDB
import threading
import time
import math

defaultTime = 12*3600*1000
password = "dfbviksbcilauebiyabv"

def getCurrentTime():
    return math.floor(time.time() * 1000)

class Database():
    def __init__(self):
        self.lock = threading.Lock()
        r = RethinkDB()
        self.r = r
        self.conn = r.connect(host= "192.168.88.245", port= 11000, user="admin", password= password)
        self.db = r.db("artists")


    def insertQuery(self, queryDict):
        defaultValues = { "id": self.r.uuid(), "created": getCurrentTime(), "updated": 0 }        
        mergedDict = defaultValues | queryDict      
        self.lock.acquire()
        result = self.db.table("accounts").insert(mergedDict).run(self.conn)
        self.lock.release()
        return result

    def insertNewAccount(self, accountType, accountId, extraData = {}):
        if (not accountType or not accountId):
            return { "status": "error", "message": "Account type or account id is missing" }

        self.lock.acquire()
        existingAcc = self.db.table("accounts").filter({"type": accountType, "accountId": accountId.lower()}).run(self.conn)
        self.lock.release()        
        if (len(list(existingAcc)) > 0):
            return {"status": "info", "message": "Account is already in the database" }

        try:
            insertObj = {"type": accountType, "accountId": accountId.lower()} | extraData
            self.insertQuery(insertObj)
            return {"status": "success", "message": f"Account {accountId} added to database"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def updateAccount(self, id, properties):
        self.lock.acquire()    
        result = self.db.table("accounts").get(id).update(properties, return_changes = True).run(self.conn)
        self.lock.release()
        return result

    def getAllAccounts(self, accountType, options = {}):
        params = options
        params["type"] = accountType
        self.lock.acquire()
        result = self.db.table("accounts").filter(options).order_by("accountId").run(self.conn)
        self.lock.release()
        return result

    def getAccountsToUpdate(self, accountType, lastUpdated = defaultTime):
        time = getCurrentTime() - lastUpdated
        self.lock.acquire()
        result = self.db.table("accounts").filter(lambda account: (account["updated"] < time) & (account["type"] == accountType) & (account["updated"] > 0)).order_by("accountId").run(self.conn)
        self.lock.release()
        return result

    def getAccountsToDownload(self, accountType):
        self.lock.acquire()
        result = self.db.table("accounts").filter(lambda account: (account["type"] == accountType) & account["updated"] == 0).order_by("accountId").run(self.conn)
        self.lock.release()
        return result
    
    def getAll(self):
        self.lock.acquire()
        result = self.db.table("accounts").order_by("accountId").run(self.conn)
        self.lock.release()
        return result


database = Database()