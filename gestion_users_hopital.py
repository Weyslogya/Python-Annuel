########################################################################
### PROJET T1 : Gestion des utilisateurs d'un hôpital en Python
### (à la manière de l'Active Directory, sans interface graphique)
###
### DECOUPAGE FONCTIONNEL :
###   1. Les classes        : Salarié (mère) et User (fille)
###   2. Les mots de passe  : génération, hashage (sha256 + sel), vérification
###   3. Les logins         : génération automatique (1ère lettre prénom + nom)
###   4. La gestion         : ajouter, modifier, supprimer, rechercher, lister
###   5. La sécurité        : connexion, verrouillage après 3 échecs
###   6. Les groupes        : les services de l'hôpital (comme les groupes AD)
###   7. Le programme principal : un menu dans la console
########################################################################

import random
import string
import hashlib

### Les services de l'hôpital (équivalent des groupes dans l'AD)
SERVICES = ["Médecine", "Infirmerie", "Administratif", "Informatique", "Direction"]

### L'annuaire : un dictionnaire { login : objet User }
### (le login est la clé car il est unique)
annuaire = {}


######################################## CLASSES ########################################

class Salarié(object):
    """Classe des salariés de l'hôpital"""

    ### Constructeur : construit et initialise un objet
    def __init__(self, nom, pnom):
        self.Nom = nom
        self.Prenom = pnom

    ### Les getters
    def get_nom(self):
        return self.Nom

    def get_pnom(self):
        return self.Prenom

    ### Les setters (avec un contrôle : pas de valeur vide)
    def set_nom(self, nouveau_nom):
        if nouveau_nom == "":
            print("Le nom de l'employé ne peut pas être vide!!!!")
        else:
            self.Nom = nouveau_nom
            print("Le nom a été modifié.")

    def set_pnom(self, nouveau_pnom):
        if nouveau_pnom == "":
            print("Le prénom de l'employé ne peut pas être vide!!!!")
        else:
            self.Prenom = nouveau_pnom
            print("Le prénom a été modifié.")


class User(Salarié):  ## la classe User hérite de Salarié (classe mère)
    """Classe des utilisateurs : un salarié qui a un compte"""

    def __init__(self, nom, pnom, login, service, pwd_hash, salt):
        Salarié.__init__(self, nom, pnom)  ### Nom et Prenom sont hérités
        self.Login = login
        self.Service = service
        self.Salt = salt              ### le sel est propre à chaque user
        self.Pwd_hash = pwd_hash      ### on ne stocke JAMAIS le mot de passe en clair
        self.Essais = 0               ### nombre d'échecs de connexion
        self.Verrouille = False       ### compte bloqué ou non

    ### getters
    def get_login(self):
        return self.Login

    def get_service(self):
        return self.Service

    ### setters
    def set_service(self, nouveau_service):
        if nouveau_service not in SERVICES:
            print("Ce service n'existe pas!!!!")
        else:
            self.Service = nouveau_service
            print("Le service a été modifié.")

    def set_pwd(self, nouveau_pwd):
        ### on génère un nouveau sel et on hashe le nouveau mot de passe
        self.Salt = generer_salt()
        self.Pwd_hash = hasher_pwd(nouveau_pwd, self.Salt)

    ### autres méthodes
    def Afficher_User(self):
        if self.Verrouille:
            etat = "VERROUILLE"
        else:
            etat = "actif"
        print("Login :", self.Login, "| Nom :", self.Nom, "| Prénom :", self.Prenom,
              "| Service :", self.Service, "| Etat :", etat)


################################ FONCTIONS : MOTS DE PASSE ################################

def generer_pwd(taille):
    """Génère un mot de passe aléatoire de la taille demandée"""
    liste_de_caractères = string.ascii_letters + string.digits + string.punctuation
    passwd = ""  ### initialement vide
    for i in range(taille):
        passwd = passwd + liste_de_caractères[random.randint(0, len(liste_de_caractères) - 1)]
    return passwd


def generer_salt():
    """Génère un sel aléatoire de 8 caractères"""
    salt = ""
    for i in range(8):
        salt = salt + random.choice(string.ascii_letters + string.digits)
    return salt


def hasher_pwd(pwd, salt):
    """Retourne l'empreinte sha256 du mot de passe + sel"""
    pwd_bytes = (pwd + salt).encode()
    return hashlib.sha256(pwd_bytes).hexdigest()


def verif_pwd(user, pwd):
    """Vérifie un mot de passe : on hashe ce qui est saisi et on compare aux empreintes"""
    return hasher_pwd(pwd, user.Salt) == user.Pwd_hash


def pwd_valide(pwd):
    """Politique de mot de passe : 8 caractères min, 1 majuscule, 1 minuscule, 1 chiffre"""
    maj = False
    minus = False
    chiffre = False
    for c in pwd:
        if c in string.ascii_uppercase:
            maj = True
        if c in string.ascii_lowercase:
            minus = True
        if c in string.digits:
            chiffre = True
    return len(pwd) >= 8 and maj and minus and chiffre


################################ FONCTIONS : LOGIN ET SAISIES ################################

def generer_login(nom, pnom):
    """Login = 1ère lettre du prénom + nom, en minuscules. Si déjà pris, on ajoute un numéro"""
    base = (pnom[0] + nom).lower().replace(" ", "")
    login = base
    numero = 1
    while login in annuaire:  ### on évite les doublons
        login = base + str(numero)
        numero = numero + 1
    return login


def saisir_non_vide(message):
    """Redemande la saisie tant que la valeur est vide"""
    while True:
        valeur = input(message).strip()
        if valeur == "":
            print("La valeur ne peut pas être vide!!!!")
        else:
            return valeur


def choisir_service():
    """Affiche les services et retourne celui choisi"""
    while True:
        for i in range(len(SERVICES)):
            print(" ", i + 1, "-", SERVICES[i])
        try:
            choix = int(input("Numéro du service : "))
            if choix < 1 or choix > len(SERVICES):
                raise ValueError
            return SERVICES[choix - 1]
        except ValueError:
            print("Choix non valide!!")


def demander_login():
    """Demande un login et retourne l'objet User correspondant (ou None)"""
    login = input("Login de l'utilisateur : ").strip().lower()
    if login in annuaire:
        return annuaire[login]
    else:
        print("Utilisateur introuvable!!")
        return None


################################ FONCTIONS : GESTION ################################

def ajouter_user():
    nom = saisir_non_vide("Nom : ").upper()
    pnom = saisir_non_vide("Prénom : ").capitalize()
    print("Choisir le service :")
    service = choisir_service()
    login = generer_login(nom, pnom)
    pwd = generer_pwd(10)  ### mot de passe temporaire
    salt = generer_salt()
    nouveau = User(nom, pnom, login, service, hasher_pwd(pwd, salt), salt)
    annuaire[login] = nouveau
    print("==> Utilisateur créé !")
    print("    Login :", login)
    print("    Mot de passe temporaire :", pwd, "(à communiquer à l'utilisateur, non stocké en clair)")


def supprimer_user():
    user = demander_login()
    if user is not None:
        confirm = input("Supprimer " + user.get_login() + " ? (o/n) : ")
        if confirm.lower() == "o":
            del annuaire[user.get_login()]
            print("Utilisateur supprimé.")
        else:
            print("Suppression annulée.")


def modifier_user():
    user = demander_login()
    if user is not None:
        print("1 - Modifier le nom")
        print("2 - Modifier le prénom")
        print("3 - Modifier le service")
        choix = input("Votre choix : ")
        if choix == "1":
            user.set_nom(input("Nouveau nom : ").strip().upper())
        elif choix == "2":
            user.set_pnom(input("Nouveau prénom : ").strip().capitalize())
        elif choix == "3":
            user.set_service(choisir_service())
        else:
            print("Choix non valide!!")


def rechercher_user():
    mot = input("Nom (ou début du nom) à rechercher : ").strip().upper()
    trouve = False
    for login in annuaire:
        if annuaire[login].get_nom().startswith(mot):
            annuaire[login].Afficher_User()
            trouve = True
    if not trouve:
        print("Aucun résultat.")


def lister_users():
    if len(annuaire) == 0:
        print("L'annuaire est vide.")
    else:
        print("Nombre d'utilisateurs :", len(annuaire))
        for login in sorted(annuaire):  ### triés par ordre alphabétique de login
            annuaire[login].Afficher_User()


def lister_par_service():
    """Affiche les membres de chaque groupe (comme les groupes de l'AD)"""
    for service in SERVICES:
        print("\n== Service", service, "==")
        vide = True
        for login in sorted(annuaire):
            if annuaire[login].get_service() == service:
                print("  -", login, "(", annuaire[login].get_pnom(), annuaire[login].get_nom(), ")")
                vide = False
        if vide:
            print("  (aucun membre)")


################################ FONCTIONS : SECURITE ################################

def connexion():
    """Simule l'ouverture de session : 3 essais maximum, puis le compte est verrouillé"""
    user = demander_login()
    if user is not None:
        if user.Verrouille:
            print("Compte verrouillé! Contactez l'administrateur.")
            return
        pwd = input("Mot de passe : ")
        if verif_pwd(user, pwd):
            user.Essais = 0
            print("==> Connexion réussie, bienvenue", user.get_pnom(), user.get_nom(), "!")
        else:
            user.Essais = user.Essais + 1
            print("Mot de passe incorrect. Essai", user.Essais, "/ 3")
            if user.Essais >= 3:
                user.Verrouille = True
                print("Trop d'échecs : le compte", user.get_login(), "est VERROUILLE.")


def changer_pwd():
    """Changement de mot de passe par l'utilisateur (il doit connaître l'ancien)"""
    user = demander_login()
    if user is not None:
        ancien = input("Ancien mot de passe : ")
        if verif_pwd(user, ancien):
            nouveau = input("Nouveau mot de passe (8 car. min, 1 majuscule, 1 minuscule, 1 chiffre) : ")
            if pwd_valide(nouveau):
                user.set_pwd(nouveau)
                print("Mot de passe modifié.")
            else:
                print("Mot de passe trop faible, il n'a pas été modifié.")
        else:
            print("Ancien mot de passe incorrect.")


def reinitialiser_pwd():
    """Action de l'administrateur : nouveau mot de passe aléatoire"""
    user = demander_login()
    if user is not None:
        pwd = generer_pwd(10)
        user.set_pwd(pwd)
        print("Nouveau mot de passe temporaire :", pwd)


def deverrouiller_user():
    user = demander_login()
    if user is not None:
        if user.Verrouille:
            user.Verrouille = False
            user.Essais = 0
            print("Le compte a été déverrouillé.")
        else:
            print("Ce compte n'est pas verrouillé.")


################################ DONNEES DE DEMONSTRATION ################################

def charger_demo():
    """Quelques utilisateurs pour la démonstration (mot de passe : Hopital2026)"""
    liste = [("MARTIN", "Sophie", "Médecine"),
             ("DUPONT", "Karim", "Infirmerie"),
             ("BERNARD", "Julie", "Administratif")]
    for nom, pnom, service in liste:
        login = generer_login(nom, pnom)
        salt = generer_salt()
        annuaire[login] = User(nom, pnom, login, service, hasher_pwd("Hopital2026", salt), salt)


###################################### FIN DES FONCTIONS ######################################

### main, programme principal
charger_demo()
print("===== Gestion des utilisateurs de l'hôpital =====")

while True:
    print("\n----------- MENU -----------")
    print("1 - Ajouter un utilisateur")
    print("2 - Modifier un utilisateur")
    print("3 - Supprimer un utilisateur")
    print("4 - Rechercher un utilisateur")
    print("5 - Lister tous les utilisateurs")
    print("6 - Lister par service")
    print("7 - Se connecter (test)")
    print("8 - Changer son mot de passe")
    print("9 - Réinitialiser un mot de passe (admin)")
    print("10 - Déverrouiller un compte (admin)")
    print("0 - Quitter")
    try:
        choix = int(input("Votre choix : "))
    except ValueError:  ### si l'utilisateur ne tape pas un nombre
        print("Erreur : saisir un nombre!!")
        continue

    if choix == 1:
        ajouter_user()
    elif choix == 2:
        modifier_user()
    elif choix == 3:
        supprimer_user()
    elif choix == 4:
        rechercher_user()
    elif choix == 5:
        lister_users()
    elif choix == 6:
        lister_par_service()
    elif choix == 7:
        connexion()
    elif choix == 8:
        changer_pwd()
    elif choix == 9:
        reinitialiser_pwd()
    elif choix == 10:
        deverrouiller_user()
    elif choix == 0:
        print("Fin du programme....")
        break
    else:
        print("Choix non valide!!")
