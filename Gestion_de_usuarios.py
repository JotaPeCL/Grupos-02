"""
Autor: Juan Pablo Campos López
Tema:POO - Microservicio de gestion de usuarios
fecha: 08/10/2024
"""

import pymongo
from pymongo.errors import OperationFailure
from decouple import config
from Usuario import Usuario
from Grupos import Grupo


class GestorUsuarios:
    def __init__(self, host=None, user="", password="", port="27017", mongo_uri=None):
        self.MONGO_USER = user
        self.MONGO_PASSWORD = password
        self.MONGO_HOST = host if host else "localhost"  # Si tiene algo host se conecta a la nube
        self.MONGO_PORT = port
        self.MONGO_URI = mongo_uri
        self.MONGO_CLIENT = None
        self.MONGO_CURSOR = None

    def conectar_mongodb(self):
        print(self.MONGO_HOST)
        try:
            if self.MONGO_HOST == 'localhost':
                self.MONGO_URI = f"mongodb://{self.MONGO_HOST}:{self.MONGO_PORT}/"
            else:
                self.MONGO_URI = "mongodb+srv://juanpcamlo20:rq9WCGvDvQESJp9t@pruebas.uwm27.mongodb.net/?retryWrites=true&w=majority&appName=Pruebas"

            # "mongodb+srv://juanpcamlo20:rq9WCGvDvQESJp9t@pruebas.uwm27.mongodb.net/?retryWrites=true&w=majority&appName=Pruebas"
            self.MONGO_CLIENT = pymongo.MongoClient(self.MONGO_URI)
            # print(self.MONGO_HOST, self.MONGO_CLIENT)
            try:
                print(self.MONGO_CLIENT.host)  # server_info() solo funciona en local
            except OperationFailure as error_operacion:
                return "Error en la operación: " + str(error_operacion)
        except pymongo.errors.ServerSelectionTimeoutError as error_tiempo:
            return "Tiempo excedido para la conexion " + str(error_tiempo)

    def registrar_usuario(self, usuario, db='db_usuarios', coleccion='usuarios'):
        self.conectar_mongodb()
        if self.MONGO_CLIENT[db][coleccion].find_one({"email": usuario.email}):
            return {"Mensaje": f"El usuario  {usuario.email} ya existe"}, 409
        self.MONGO_CLIENT[db][coleccion].insert_one(usuario.to_dict())
        self.cerrar_conexion_mongodb()
        return {"Mensaje": "usuario registrado correctamente"}, 201

    def restabecer_passwrd(self, usuario, nuevo_password, db='db_usuarios', coleccion='usuarios'):
        self.conectar_mongodb()
        usuario.hashed_password = nuevo_password
        self.MONGO_CLIENT[db][coleccion].update_one({"email": usuario.email},
                                                    {"$set": {"password": usuario.hashed_password}})
        self.cerrar_conexion_mongodb()
        return {"Mensaje": f"usuario con email :{usuario.email} se actualizo correctamente"}, 201

    def obtener_usuario_por_email(self, email, db='db_usuarios', coleccion='usuarios'):
        self.conectar_mongodb()
        usr = self.MONGO_CLIENT[db][coleccion].find_one({"email": email})
        if usr:
            self.cerrar_conexion_mongodb()
            return Usuario(usr['nombre'], usr['email'], usr['id_grupo'], password=None, hashed_password=usr['password'])
        self.cerrar_conexion_mongodb()
        return None

    def burcar_por_id(self, id_grupo, db='db_usuarios', coleccion='grupos'):
        self.conectar_mongodb()
        grupo = self.MONGO_CLIENT[db][coleccion].find_one({"grupo": id_grupo})
        if grupo:
            self.cerrar_conexion_mongodb()
            return grupo
        self.cerrar_conexion_mongodb()
        return None

    def regresa_conexion_mongodb(self):
        """ Regresa la conexión a la Base de Datos de MongoDB"""
        return self.MONGO_CLIENT

    def cerrar_conexion_mongodb(self):
        """ Cierra la conexión a la Base de Datos de MongoDB   """
        try:
            if self.MONGO_CLIENT:
                self.MONGO_CLIENT.close()
        except Exception:
            print("ERROR al cerrar la conexion a la Base de Datos MongoDB")


def permisos(func):
    def wrapper(grupo_id, *args, **kwargs):
        gestor_usuarios = GestorUsuarios() 
        grupo_data = gestor_usuarios.burcar_por_id(grupo_id)
        if grupo_data:
            grupo = Grupo(grupo_data['_id'], grupo_data['nombre'], grupo_data['permisos'])
            if grupo.tiene_permiso('Ver-Pedidos'):
                return func(grupo, *args, **kwargs)
            else:
                return "Acceso denegado: No tienes el permiso 'Ver-Pedidos'"
        else:
            return "Grupo no encontrado"

    return wrapper


@permisos
def ver_pedidos(grupo):
    return "Este grupo puede ver los pedidos."



print(ver_pedidos(400))
"""

objCon.conectar_mongodb()
objuser1=Usuario("Pablo","Pablo@gmail.com",password="123456")
objuser2=Usuario("Carmen","Carmen@gmail.com",password="123456")
Usuario("Juan Pérez",
    email="juan.perez@example.com",
    id_grupo=100,  # ID del grupo (por ejemplo, 100 para Clientes)
    password="mi_contraseña_segura")
"""
"""
objCon = GestorUsuarios()
obj = Usuario("Juan Pérez",
              "juan.perez@example.com",
              100,
              "Contraseña")


objCon.registrar_usuario(obj)
# objCon.registrar_usuario(objuser2)

print(objCon.obtener_usuario_por_email("juan.perez@example.com"))
"""

# objCon.cerrar_conexion_mongodb()
