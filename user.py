import string
import hashlib
import random
import secrets

class Salarie():
""" Classe des salarié"""

	def __init__(self, nom, prenom):
		"""  Crée le salarié avec un nom et prénom """
		self.nom = nom
		self.prenom = prenom


	def get_nom(self):
		""" Retourne le nom """
		return self.nom


	def get_prenom(self):
		""" Retourne le prénom """
		return self.prenom


	def set_nom(self, nv_nom):
		"""
		Modifie le nom

		Paramètre :
		-----------
		nv_nom : str
		Nouveau nom
		  """
		if nv_nom.strip() == "":
			raise ValueError("Le nom de l'employé ne peut pas être vide !")
		self.nom = nv_nom

	def set_prenom(self, nv_prenom):
		"""
		Modifie le prénom

		Paramètre :
		-----------
		nv_prenom : str
		Nouveau prénom
		"""
		if nv_prenom.strip() == "":
			raise ValueError("Le prénom ne peut pas être vide !")
		self.prenom = nv_prenom

class User(Salarie):
	def __init__(self, nom, prenom, login, passwd):
		super.__init__(self, nom, prenom)
		self.login = login
		self.passwd = passwd

	def get_login(self):
		return self.login

	def get_passwd(self):
		return self.passwd

	def set_login(self, nv_login):
		if nv_login.strip() == "":
			raise ValueError("Le login ne peut pas être vide !")
		self.login = nv_login

	def set_passwd(self, nv_passwd):
		if nv_passwd.strip() == "":
			raise ValueError("Le mot de passe ne peut pas être vide ! ")
		self.passwd = nv_passwd

	def gen_passwd(self, size):
		passwd = ""
		caracteres = string.ascii_letters + string.digits + string.punctuation

		for i in range(size):
			passwd += caracteres[random.randint(0, len(caracteres) -1)]

		print("==> Le mot de passe généré est :", passwd)
		return passwd

	def hash_passwd(self, passwd):
		salt = secrets.token_hex(16)
		passwd_bytes = (passwd + salt).encode()
		passwd_hashed = hashlib.sha256(passwd_bytes).hexdigest()

		print("==> Mot de passe hashé en sha256 : ", passwd_hashed)

		return f"{salt}: {passwd_hashed}"



