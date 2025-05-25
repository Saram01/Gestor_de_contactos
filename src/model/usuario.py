import bcrypt
import re
from src.model.contactos import Contacto
from src.model.excepciones import (
    InvalidNameError,
    InvalidEmailError,
    InvalidPasswordError,
)

class Usuario:
    """
    Representa un usuario que puede registrarse y manejar contactos.
    """
    def __init__(self, nombre_usuario: str, email: str = None, password: str = None):
        if not self.validar_nombre(nombre_usuario):
            raise InvalidNameError("Nombre de usuario inválido.")
        if not self.validar_password(password):
            raise InvalidPasswordError("Contraseña insegura.")
        self.nombre_usuario = nombre_usuario
        self.email = email
        self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        self.contactos = []

    def verificar_contraseña(self, contraseña: str) -> bool:
        return bcrypt.checkpw(contraseña.encode(), self.password.encode())

    def iniciar_sesion(self, nombre_usuario: str, contraseña: str) -> bool:
        return self.nombre_usuario.lower() == nombre_usuario.lower() and self.verificar_contraseña(contraseña)

    def agregar_contacto(self, contacto: Contacto):
        if any(c.email == contacto.email for c in self.contactos):
            raise ValueError(f"El contacto con el correo {contacto.email} ya existe.")
        self.contactos.append(contacto)

    @property
    def obtener_contactos(self):
        return self.contactos

    @staticmethod
    def validar_email(email: str) -> bool:
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(pattern, email) is not None

    @staticmethod
    def validar_nombre(nombre: str) -> bool:
        pattern = r"^[a-zA-Z0-9_-]{3,20}$"
        return bool(re.match(pattern, nombre.strip()))

    @staticmethod
    def validar_password(password: str) -> bool:
        return len(password) >= 6
