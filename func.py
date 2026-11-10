import string
import random
import hashlib

def gen_login(nom, prenom):
    """
    Génère un identifiant

    Paramètres :
    ------------
    nom : str
        Nom de la personne

    prenom : str
        Prenom de la personne

    Retourne :
    ----------
    str
        Génère un identifiant au format "[premiere lettre du prenom].[nom de famille]"
    """

    login = prenom[0].lower() + "." + nom.lower()

    print("==> Identifiant : ", login)

    return login

def gen_passwd(size):
    """
    Génère un mot de passe aléatoire en respectant les règles de sécurité.

    Paramètres :
    ------------
    size : int
        La longueur souhaitée pour le mot de passe

    Retourne :
    ----------
    str
        Le mot de passe généré sous forme de chaîne de caractères    
    """
    passwd = ""
    caracteres = string.ascii_letters + string.digits + string.punctuation
   
    for i in range(size):
        passwd += caracteres[random.randint(0, len(caracteres) - 1)]

    print("==> Le mot de passe généré :", passwd)
   
    return passwd


def hash_passwd(passwd) :
    """
    Hash un mot de passe avec l'algorithme sha256

    Paramètres :
    ----------
   
    passwd : int
        Le mot de passe que l'on souhaite hashé

    Retourne :
    ----------
   
        Le mot de passe hashé en sh256
   
    """
    salt = "dd"
    passwd_bytes = (passwd + salt).encode()

    passwd_hashed = hashlib.sha256(passwd_bytes).hexdigest()

    print("==> mot de passe hashé sha256 : ", passwd_hashed)

    return passwd_hashed

identifiant = gen_login("DRAME", "Fodé")

mdp = gen_passwd(16)

hashed = hash_passwd(mdp)
