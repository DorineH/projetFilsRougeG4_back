import psycopg2
import sys
import codecs

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

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

def getUserByName(name):
    db_connection = get_db_connection()
    if db_connection is None: 
        return None
    cursor = db_connection.cursor()
    # del resultsExportUsers[:]
    postgresSQL = "SELECT name, password FROM public.t_users WHERE name = %s"
    try:
        cursor.execute(postgresSQL, (name,))
        result = cursor.fetchone()
        if result:
            return {"name": result[0], "password": result[1]}
        return None
    except psycopg2.Error as e:
        print("PostgresSQL Error: %s" % str(e))
        return None
    finally:
        cursor.close()
        db_connection.close()
 

def getUsers():
    db_connection = get_db_connection()
    if db_connection is None:
        return None
    cursor = db_connection.cursor()
    del resultsExportUsers[:]
    postgresSQL = "SELECT * FROM public.t_users"
    try:
        cursor.execute(postgresSQL)
        results = cursor.fetchall()

        if results:
            print(f"{len(results)} utiliseteurs trouvés")
        else:
            print("Aucun utilisateur trouvé")
        for row in results:
            item = {
                "name": row[0],
                "password": row[1]
            }
            resultsExportUsers.append(item)
    except psycopg2.Error as e:
        print ("postgresSQL Error [%d]: %s" % (e.args[0], e.args[1]))
        print ("postgresSQL Error: %s" % str(e))
    finally:
        cursor.close()
        db_connection.close()
            

def createUser(user):
    connection = get_db_connection()
    if connection is None:
        return
    cursor = connection.cursor()
    sql = "INSERT INTO public.t_users (name, password) VALUES (%s, %s)"
    try:
        cursor.execute(sql, (user['name'], user['password']))
        connection.commit()
        print("Utilisateur crée avec succés")
    except psycopg2.Error as e:
        print ("PostgreSQL  Error: %s" % str(e))
        connection.rollback()
    finally:
        cursor.close()
        connection.close()
