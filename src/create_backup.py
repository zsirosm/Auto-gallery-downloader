from downloader.database import database

records = database.getAll()

print(records)

def returnExtra(account):
    type = account.get("type")
    if type == "kemonoparty":
        extraPath = account.get("extraPath")
        domain = extraPath.get("domain")
        return domain
    else:
        return "undefined"


with open("dpbackup.txt", "w") as outputFile:
    outputFile.write(f"uuid - accountId - type - created - updated - extraPath.domain \n")
    
    for account in records:
        outputFile.write(f"{account.get('id')} - {account.get('accountId')} - {account.get('type')} - {account.get('created')} - {account.get('updated')} - {returnExtra(account)} \n")