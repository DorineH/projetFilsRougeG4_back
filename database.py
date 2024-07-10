import psycopg2
import sys
import codecs

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

# connection à la base de donnée pgAdmin
def get_db_connection():
    try: 
        db = psycopg2.connect(
            host='localhost',
            port=5432,
            dbname='postgres', 
            user='postgres', 
            password='postgres', 
            connect_timeout=10,
            sslmode='prefer'
        )
        db.set_client_encoding('UTF8')
        print("Connexion db réussie")
        return db 
    except (Exception, psycopg2.DatabaseError) as error:
        print("Erreur lors de la connexion à la base de données", error)
        return None

resultsExportUsers = []

# Récuperer un utilisateur par son nom (mongoDB OK)
def get_user_by_pseudo(pseudo):
    print('getUserByPseudo')
    db_connection = get_db_connection()
    print('db_connection', db_connection)
    if db_connection is None: 
        return None
    cursor = db_connection.cursor()
    # del resultsExportUsers[:]
    postgresSQL = "SELECT prenom, nom, pseudo, password FROM public.t_users WHERE pseudo = %s"
    try:
        cursor.execute(postgresSQL, (pseudo,))
        result = cursor.fetchone()
        if result:
            return {"prenom": result[0], "nom": result[1], "pseudo": result[2], "password": result[3]}
        return None
    except psycopg2.Error as e:
        print("PostgresSQL Error: %s" % str(e))
        return None
    finally:
        cursor.close()
        db_connection.close()
 
#  Récupper tous les utilisateurs de la base de donnée (mongoDB OK)
def getUsers():
    print('getUsers')
    db_connection = get_db_connection()
    print('db_connection2', db_connection)

    if db_connection is None:
        return None
    cursor = db_connection.cursor()
    del resultsExportUsers[:]
    postgresSQL = "SELECT * FROM public.t_users"
    try:
        cursor.execute(postgresSQL)
        results = cursor.fetchall()

        if results:
            print(f"{len(results)} utilisateurs trouvés")
        else:
            print("Aucun utilisateur trouvé")
        for row in results:
            item = {
                "prenom": row[0],
                "nom": row[1],
                "pseudo": row[2],
                "password": row[3]
            }
            resultsExportUsers.append(item)
    except psycopg2.Error as e:
        print ("postgresSQL Error [%d]: %s" % (e.args[0], e.args[1]))
        print ("postgresSQL Error: %s" % str(e))
    finally:
        cursor.close()
        db_connection.close()
            
#  Créer une utilisateur dans la base de données
def createUser(user):
    connection = get_db_connection()
    if connection is None:
        return
    cursor = connection.cursor()
    sql = "INSERT INTO public.t_users (prenom, nom, pseudo, password) VALUES (%s, %s, %s, %s)"
    try:
        cursor.execute(sql, (user['prenom'], user['nom'], user['pseudo'], user['password']))
        connection.commit()
        print("Utilisateur crée avec succés")
    except psycopg2.Error as e:
        print ("PostgreSQL  Error: %s" % str(e))
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

# Récupere le score avec le pseudo
# def get_scores_by_pseudo():

# Sauvegardes les scores
# def save_score():

