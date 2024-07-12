import pymongo
from datetime import datetime
import pprint

uri = "mongodb://localhost:27017/"
client = pymongo.MongoClient(uri)

mydb = client["projetFilRouge"]
mycol = mydb["users"]
mycolScore = mydb["scores"]
# db = client.projetFilRouge
# collection = db.users
# data = datetime

mydict = { "prenom": "Jean", "nom": "Dupont", "pseudo": "jeanD", "password": "passwordJean!11" }
mydictScore = { "pseudo": "DodoTheBest", "score": 200, "date": "10/07/2024" }

dblist = client.list_database_names()
collist = mydb.list_collection_names()

# insertion dans la table, pour inserer plusieurs en meme temps faire insert_many()
x = mycolScore.insert_one(mydictScore)

# renvoie le premier element de la collection (ici users)
y = mycol.find_one()

myquery = { "pseudo": "DodoTheBest" }

mydoc = mycol.find(myquery)

try:
    client.admin.command("ping")
    print("Connected successfully")

    # récupere les noms db
    print(dblist) 
    if "projetFilRouge" in dblist:
        print("Database exist !")

    # récupere  les collection de la db
    print(collist) 
    if "users" in collist:
        print("Collection exist !")

    if "scores" in collist:
        print("Collection exist !")

    print(x)

    # print(y)

    # renvoie tout l'objet de la collection users
    # for z in mycol.find():
    #     print (z)

    # récupere toute les données de db
    # for a in mycol.find({}, {"_id": 0, "prenom": 1, "nom": 2, "pseudo": 3, "password": 4}):
    #     print (a)

    # récupere les donnée en fonction d'une column (ici pseudo)
    for b in mydoc:
        print(b)

    
    # client.close()

except Exception as e:
    raise Exception(
        "The following error occurred: ", e)
