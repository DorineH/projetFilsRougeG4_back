import pymongo
from datetime import datetime

resultsExportUsers = []

#  Connection à la base de donnée mongoDB
def get_db_connection():
    try:
        uri = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(uri)
        mydb = client["projetFilRouge"]
        return mydb
    except  Exception as e:
        print(f"Erreur de la connexionà la base de donnée: {e}")
        return None

#  Récupere tous les utilisateurs 
def getUsersMongoDB():
    print('getUsers')
    db_connection = get_db_connection()

    if db_connection is None:
        return None
    
    mycollection = db_connection["users"]

    del resultsExportUsers[:]

    try:
        results = mycollection.find()
        results = list(results)

        if results:
            print(f"{len(results)} utilisateurs trouvés")
        else:
            print("Aucun utilisateur trouvé")

        for row in results:
            item = {
                "prenom": row.get("prenom", ""),
                "nom": row.get("nom", ""),
                "pseudo": row.get("pseudo", ""),
                "password": row.get("password", "")
            }
            resultsExportUsers.append(item)
    except Exception as e:
        print ("mongodb Error: {e}" )
        print("error mongodb get users")
    finally:
        db_connection.client.close()


# Récuperer un utilisateur par son nom  # MongoDB ok
def getUserByPseudo(pseudo):
    print('getUserByPseudo')
    db_connection = get_db_connection()

    if db_connection is None:
        return None
    
    mycollection = db_connection["users"]
    print('mycollection get user by pseudo ')
    print(mycollection)
   
    try:
        myquery = { "pseudo": pseudo }
        result = mycollection.find_one(myquery)
        print('result ', result)

        if result:
            return {
                "prenom": result.get("prenom", ""),
                "nom": result.get("nom", ""),
                "pseudo": result.get("pseudo", ""),
                "password": result.get("password", "")
            }
        return None
    
    except Exception as e:
        print("MongoDB get user by pseudo Error: ", {e})
        return None
    finally:
        db_connection.client.close()

# Créer un user 
def createUserMongoDB(user):
    print('createUserMongoDB')
    db_connection = get_db_connection()

    if db_connection is None:
        return None
    
    mycollection = db_connection["users"]
   
    try:
        myquery = {
            "prenom": user['prenom'],
            "nom": user['nom'],
            "pseudo": user['pseudo'],
            "password": user['password']
        }
        result = mycollection.insert_one(myquery)        
        print('Utilisateur crée avec succès')
        print(result)
    
    except Exception as e:
        print("MongoDB Error: {e}" )
        return None
    finally:
        db_connection.client.close()

# Enregistrement des scores
def saveScore(pseudo, score):
    print('saveScore')
    db_connection = get_db_connection()
    print('db_connection ', db_connection)

    if db_connection is None:
        return None
    
    mycollection = db_connection["scores"]

    try: 
        myquery = {
            "pseudo": pseudo,
            "score": score,
            "date": datetime.utcnow()
        }
        result = mycollection.insert_one(myquery) 
        return result
    except Exception as e:
        print("MongoDB save score Error: ", {e} )
        return None
    finally:
        db_connection.client.close()

#  Récupere les scores
def getScoresByPseudo(pseudo):
    print('getScoresByPseudo')  # print  ici
    db_connection = get_db_connection()
    print('db_connection ', db_connection) # print  ici
    print(pseudo) # print  ici

    if db_connection is None:
        return None
    
    mycollection = db_connection["scores"]
    print('mycollection get score by pseudo ') # print  ici
    print(mycollection) # print  ici

    try: 
        myquery = {"pseudo": pseudo}
        print(myquery) # print  ici
        scores_by_pseudo = list(mycollection.find(myquery))
        # for u in list(mycollection.find(myquery)):
        #     print(u)
        if scores_by_pseudo:
            scores_list = []
            for score in scores_by_pseudo:
                scores_list.append({
                    "pseudo": score.get("pseudo", ""),
                    "score": score.get("score", ""),
                    "date": score.get("date", "")
                })
            return scores_list
        return None
    
    except Exception as e:
        print("MongoDB get scores by pseudo Error: ", {e} )
        return None
    finally:
        db_connection.client.close()



# test pour lancer les fonctions seuls
# getUsersMongoDB()

pseudo = 'DodoTheBest'
user = getUserByPseudo(pseudo)
print('55555555555555') # ok
print(user) # ok 

# newUser = { "prenom": "Jean", "nom": "Dupont", "pseudo": "jeanD", "password": "passwordJean!11" }
# userCreated = createUserMongoDB(newUser)
# print(userCreated)

# print('ffffffffffffffffff')
# print(resultsExportUsers)

# pseudo = 'DodoTheBest'
# score = '10'
# x = getScoresByPseudo(pseudo)
# y = saveScore(pseudo, score)
# print('rrrrrrrrrrrrrrrrrrrr')
# print(x)
# print(y)


