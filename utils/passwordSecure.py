maj = False
minu = False
digit = False
password = ''

def password_secure(password):
    while True:
        # password = input("Entrez un mot de passe :")
        print(password)
        if len(password) < 8:
            print("Le mot de passe doit contenir au moins 8 caractère")
            return False

        if len(password) > 20:
            print("Le mot de passe doit contenir moins de 20 caractère")
            return False

        for i in password:
            if i.isupper():
                maj = True
                break
        if not maj:
            print("Le mot de passe doit contenir au moin une majuscule")
            return False

        for i in password:
            if i.islower():
                minu = True
                break
        if not minu:
            print("Le mot de passe doit contenir au moins une minuscule")
            return False

        for i in password:
            if i.isdigit():
                digit = True
                break
        if not digit:
            print("Le mot de passe doit contenir au moins un nombre")
            return False

        print("Le mot de passe est valide")
        return True

        # confirmation = input("Entrez une deuxiéme fois le même mot de passe : ")
        # if confirmation == password:
        #     print("Mot de passe correct")
        #     break
        # print("Les deux mots de passe ne correspondent pas")

if __name__ == '__main__':
    password_secure(password=password)