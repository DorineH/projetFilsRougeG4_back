import pymongo

resultsExportUsers = []

#  connection à la base de donnée mongoDB
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


# Récuperer un utilisateur par son nom 
def getUserByPseudo(pseudo):
    print('getUserByPseudo')
    db_connection = get_db_connection()

    if db_connection is None:
        return None
    
    mycollection = db_connection["users"]
   
    try:
        myquery = { "pseudo": pseudo }
        result = mycollection.find_one(myquery)
        print(result)

        if result:
            return {
                "prenom": result.get("prenom", ""),
                "nom": result.get("nom", ""),
                "pseudo": result.get("pseudo", ""),
                "password": result.get("password", "")
            }
        return None
    
    except Exception as e:
        print("MongoDB Error: {e}" )
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



# test pour lancer les fonctions seul
# getUsersMongoDB()

# pseudo = 'DodoTheBest'
# user = getUserByPseudo(pseudo)
# print(user)

# newUser = { "prenom": "Jean", "nom": "Dupont", "pseudo": "jeanD", "password": "passwordJean!11" }
# userCreated = createUserMongoDB(newUser)
# print(userCreated)

# print('ffffffffffffffffff')
# print(resultsExportUsers)

