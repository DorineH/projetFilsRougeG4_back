from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
password = ''
hashed_password = ''

# Fonction pour hacher un mot de passe
def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

# Fonction pour vérifier un mot de passe haché
def check_password(hashed_password, password):
    return bcrypt.check_password_hash(hashed_password, password)

if __name__ == '__main__':
    hash_password(password)
    check_password(hashed_password, password)