import string
import hashlib
import random

class Salarie():
""" Classe des salarié"""

	def __init__(self, nom, prenom, login, passwd_hashed, ville, mail, profil, etat):
		"""  Crée le salarié avec un nom et prénom """
		self.nom = nom
		self.prenom = prenom
		self.login = login
		self.passwd = passwd_hashed
		self.ville = ville
		self.mail = mail
		self.profil = profil
		self.etat = etat

	def get_nom(self):
		""" Retourne le nom """
		return self.nom


	def get_prenom(self):
		""" Retourne le prénom """
		return self.prenom
         
	def get_login(self):
		"""Retourne le login """

	def get_passwd(self):
		""" Retourne le mot de passe hashé """
		return self.passwd

	def get_ville(self):
		""" Retourne la ville """
		return self.ville

	def get_mail(self):
		""" Retourne le mail """ 
		return self.mail

	def get_profil(self):
		""" Retourne le profil """
		return self.profil

	def get_etat(self):
		""" Retourne l' etat """
		return self.etat


	def set_nom(self, nv_nom):
		"""
		Modifie le nom

		Paramètre :
		-----------
		
		nv_nom : str
		Nouveau nom
		
		"""
		if nv_nom.strip() == "":
			raise ValueError("Le nouveau nom de l'employé ne peut pas être vide !")
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
			raise ValueError("Le nouveau prénom ne peut pas être vide !")
		self.prenom = nv_prenom

	def set_login(self, nv_login):
		""" Modifie le login

		Paramètre :
		-----------
		
		nv_login : str
		Nouveau login
		
		"""
		if nv_login.strip == "":
			raise ValueError("Le nouveau login ne peut pas être vide !")
		self.login = nv_login

	def set_passwd(self, nv_passwd):
		""" Modifie le mot de passe 
		
		Paramètre :
		-----------
		
		nv_passwd : str
		Nouveau mot de passe hashé
		
		"""
		if nv_passwd.strip == "":
			raise ValueError("Le nouveau mot de passe ne peut pas être vide !")
		self.passwd = nv_passwd

	def set_ville(self, nv_ville):
		""" Modifie la ville 
		
		Paramètre :
		-----------

		nv_ville : str
		Nouvelle ville

		"""
		if nv_ville.strip == "":
			raise ValueError("La nouvelle ville ne peut pas être vide !")
		self.ville = nv_ville

	def set_mail(self, nv_mail):
		""" Modifie le mail
		
		Paramètre :
		-----------
		
		nv_mail : str
		Nouveau mail

		"""
		if nv_mail.strip() == "":
			raise ValueError("Le nouveau mail ne peut pas être vide")
		self.mail = nv_mail


	def set_profil(self, nv_profil):
		""" Modifie le profil

		Paramètre :
		-----------

		nv_profil : str
		Nouveau profil

		"""
		if nv_profil.strip() == "":
			raise ValueError("Le nouveau profil ne peut pas être vide")
		self.profil = nv_profil 

	
	def set_etat(self, nv_etat):
		""" Modifie l'état

		Paramètre : 
		-----------

		nv_etat : str
		Nouvel état

		"""
		if nv_etat.strip() == "":
			raise ValueError("Le nouvel état ne peut pas être vide !")
		self.etat = nv_etat
