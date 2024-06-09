from flask_bcrypt import Bcrypt
# import bcrypt

bcrypt = Bcrypt()

# Fonction pour hacher un mot de passe
def hash_password(password):
    hashed = bcrypt.generate_password_hash(password)
    return hashed.decode('utf-8')

# Fonction pour vérifier un mot de passe haché
def check_password(hashed_password, password):
    hashed = bcrypt.check_password_hash(hashed_password, password)
    return hashed
