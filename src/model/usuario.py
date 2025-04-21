import re
import bcrypt
from src.model.contactos import Contacto
from src.model.excepciones import (
    InvalidNameError,
    InvalidEmailError,
    InvalidPasswordError,
)

class Usuario:
    """
    Representa un usuario del sistema, que puede almacenar una lista de contactos
    y manejar funciones de validación, autenticación y gestión de contactos personales.
    """

    def __init__(self, nombre: str, email: str, password: str):
        """
        Inicializa un nuevo usuario con validaciones de nombre, correo y contraseña.

        Args:
            nombre (str): Nombre del usuario.
            email (str): Correo electrónico del usuario.
            password (str): Contraseña en texto plano.

        Raises:
            InvalidNameError: Si el nombre está vacío o contiene caracteres no permitidos.
            InvalidEmailError: Si el email está vacío o no cumple el formato.
            InvalidPasswordError: Si la contraseña es inválida o demasiado corta.
        """
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
        self.password = self.encriptar_contraseña(password)
        self.contactos = []

    @staticmethod
    def encriptar_contraseña(contraseña: str) -> bytes:
        """
        Encripta una contraseña utilizando bcrypt.

        Args:
            contraseña (str): Contraseña en texto plano.

        Returns:
            bytes: Contraseña encriptada.
        """
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(contraseña.encode(), salt)

    def verificar_contraseña(self, contraseña: str) -> bool:
        """
        Verifica si una contraseña coincide con la contraseña encriptada del usuario.

        Args:
            contraseña (str): Contraseña en texto plano.

        Returns:
            bool: True si la contraseña es válida, False si no lo es.
        """
        return bcrypt.checkpw(contraseña.encode(), self.password)

    def iniciar_sesion(self, email: str, contraseña: str) -> bool:
        """
        Verifica las credenciales del usuario para iniciar sesión.

        Args:
            email (str): Correo electrónico.
            contraseña (str): Contraseña en texto plano.

        Returns:
            bool: True si las credenciales coinciden, False en caso contrario.
        """
        return self.email.lower() == email.lower() and self.verificar_contraseña(contraseña)

    def agregar_contacto(self, contacto: Contacto):
        """
        Agrega un nuevo contacto al usuario si no está duplicado por correo.

        Args:
            contacto (Contacto): Objeto Contacto a agregar.

        Raises:
            ValueError: Si ya existe un contacto con el mismo email.
        """
        if any(c.email == contacto.email for c in self.contactos):
            raise ValueError(f"El contacto con el correo {contacto.email} ya existe.")
        self.contactos.append(contacto)

    @property
    def obtener_contactos(self):
        """
        Devuelve la lista de contactos del usuario.

        Returns:
            list: Lista de objetos Contacto.
        """
        return self.contactos

    @staticmethod
    def validar_email(email: str) -> bool:
        """
        Valida el formato de un correo electrónico.

        Args:
            email (str): Correo a validar.

        Returns:
            bool: True si el email es válido, False en caso contrario.
        """
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(pattern, email) is not None

    @staticmethod
    def validar_nombre(nombre: str) -> bool:
        """
        Valida que un nombre solo contenga letras y espacios.

        Args:
            nombre (str): Nombre a validar.

        Returns:
            bool: True si el nombre es válido, False si contiene caracteres no permitidos.
        """
        pattern = r"^[A-Za-z\s]+$"  
        return bool(re.match(pattern, nombre.strip()))
