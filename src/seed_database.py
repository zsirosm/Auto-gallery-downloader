from rethinkdb import RethinkDB

password = "dfbviksbcilauebiyabv"

r = RethinkDB()
connection = r.connect(host= "192.168.88.245", port= 11000, user="admin", password= password)


try:
    result = r.db_create("artists").run(connection)
    print(result)
except Exception as e:
    print(e.message)

db = r.db("artists")

try:
    result = db.table_create("artists").run(connection)
    print(result)
except Exception as e:
    print(e.message)

try:
    result = db.table_create("accounts").run(connection)
    print(result)
except Exception as e:
    print(e.message)
