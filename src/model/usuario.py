from src.model.contactos import Contacto

class Usuario:
    def __init__(self, nombre: str, email: str, contraseña: str):
        self.nombre = nombre
        self.email = email
        self.contraseña = contraseña
        self.contactos = []

    def agregar_contacto(self, contacto: Contacto):
        self.contactos.append(contacto)

    def obtener_contactos(self):
        return self.contactos