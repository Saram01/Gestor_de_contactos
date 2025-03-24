import re
import bcrypt
from src.model.contactos import Contacto 
from src.model.excepciones import (
    InvalidNameError,
    InvalidEmailError,
    InvalidPasswordError,
)

class Usuario:
    def __init__(self, nombre: str, email: str, password: str):
        if not nombre.strip():
            raise InvalidNameError("El nombre no puede estar vacío.")
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$", nombre):
            raise InvalidNameError(f"Nombre inválido: {nombre}")
        
        if not email.strip():
            raise InvalidEmailError("El correo electrónico no puede estar vacío.")
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
            raise InvalidEmailError(f"Correo electrónico inválido: {email}")
        
        if not password.strip():
            raise InvalidPasswordError("La contraseña no puede estar vacía o compuesta solo por espacios.")
        if len(password) < 8:
            raise InvalidPasswordError("La contraseña debe tener al menos 8 caracteres.")

        self.nombre = nombre.strip()
        self.email = email.strip()
        self.contraseña = self.encriptar_contraseña(password)
        self.contactos = [] 


    @staticmethod
    def validar_email(email: str) -> bool:
        import re
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(pattern, email) is not None

    @staticmethod
    def validar_nombre(nombre: str) -> bool:
        import re
        pattern = r"^[A-Za-z\s]+$"  
        return bool(re.match(pattern, nombre.strip()))

    @staticmethod
    def encriptar_contraseña(contraseña: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(contraseña.encode(), salt).decode()

    def verificar_contraseña(self, contraseña: str) -> bool:
        return bcrypt.checkpw(contraseña.encode(), self.contraseña.encode())

    def iniciar_sesion(self, email: str, contraseña: str) -> bool:
        if self.email.lower() == email.lower() and self.verificar_contraseña(contraseña):
            return True
        return False

    def agregar_contacto(self, contacto: Contacto):
        if any(c.email == contacto.email for c in self.contactos):
            raise ValueError(f"El contacto con el correo {contacto.email} ya existe.")
        self.contactos.append(contacto)

    @property
    def obtener_contactos(self):
        return self.contactos

