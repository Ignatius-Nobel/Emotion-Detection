import pymongo
client = pymongo.MongoClient()

mydb = client["mydb"]

mycol = mydb["people"]

data = {'name':'John','age':30}
mycol.insert_one(data)

datalist = [{'name':'Jane','age':40},{'name':"Mark"}]
mycol.insert_many(datalist)