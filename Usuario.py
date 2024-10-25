"""
Autor: Juan Pablo Campos López
Tema:POO - Microservicio de gestion de usuarios
fecha: 08/10/2024
"""
from werkzeug.security import generate_password_hash, check_password_hash


class Usuario:
    def __init__(self, nombre, email,id_grupo, password=None,hashed_password=None):
        self.__nombre = nombre
        self.__email = email
        self.__hashed_password =self.__hash_password(password) if password else hashed_password
        self.__id_grupo = id_grupo

    def __str__(self):
        return f'Nombre: {self.__nombre}, Email: {self.__email}, Password: {self.__hashed_password}'

    @property
    def nombre(self):
        return self.__nombre

    @property
    def email(self):
        return self.__email

    @property
    def hashed_password(self):
        return self.__hashed_password

    @property
    def id_grupo(self):
        return self.__id_grupo

    @hashed_password.setter
    def hashed_password(self, password):
        self.__hashed_password = self.__hash_password(password)

    def __hash_password(self,password):
        if password:
            return generate_password_hash(password, method='pbkdf2:sha256')

    def verificar_password(self, password):
        return check_password_hash(self.__hashed_password, password)

    def to_dict(self):
        return {
            'nombre': self.__nombre,
            'email': self.__email,
            'password':self.__hashed_password,
            'id_grupo': self.__id_grupo
        }




objuser=Usuario('Juan','juan@gmail.com','12345')
#print(objuser.to_dict())