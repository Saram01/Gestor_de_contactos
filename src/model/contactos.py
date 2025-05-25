import re
from src.model.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from src.model.excepciones import (InvalidEmailError, InvalidPhoneNumberError, InvalidEmailTooLong, ContactError)
from src.model.db import Base

try:
    from src.model.db import Base
except ImportError:
    Base = declarative_base()

class Contacto(Base):
    __tablename__ = 'contacto'
    __table_args__ = {'extend_existing': True}
    """
    Clase que representa un contacto dentro del sistema de gestión.

    Atributos:
        nombre (str): Nombre del contacto.
        telefono (str): Número de teléfono del contacto (debe tener 10 dígitos).
        email (str): Correo electrónico del contacto.
        categoria (str): Categoría del contacto, por defecto "Sin categoría".

    Excepciones:
        ContactError: Si el nombre está vacío o contiene caracteres no permitidos.
        InvalidPhoneNumberError: Si el número de teléfono no es válido.
        InvalidEmailError: Si el email tiene un formato inválido.
        InvalidEmailTooLong: Si el email excede la cantidad máxima de caracteres.
    """

    __tablename__ = 'contacto'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    categoria = Column(String(30))
    email = Column(String(100), unique=True)
    telefono = Column(String(20), unique=True)
    usuario_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    usuario = relationship("Usuario", back_populates="contactos")


    def __init__(self, nombre: str, telefono: str, email: str, categoria: str = "Sin categoría", usuario_id: int = None):
        """
        Inicializa un nuevo contacto validando sus campos.

        Args:
            nombre (str): Nombre del contacto.
            telefono (str): Número de teléfono.
            email (str): Correo electrónico.
            categoria (str, opcional): Categoría del contacto. Por defecto es "Sin categoría".
            usuario_id (int, opcional): ID del usuario dueño del contacto.

        Raises:
            ContactError: Si el nombre está vacío o tiene caracteres no permitidos.
            InvalidPhoneNumberError: Si el teléfono no tiene 10 dígitos.
            InvalidEmailError: Si el email no es válido.
            InvalidEmailTooLong: Si el email supera los caracteres permitidos.
        """
        if not nombre.strip():
            raise ContactError("El nombre no puede estar vacío o compuesto solo por espacios.")
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$", nombre):
            raise ContactError("El nombre contiene caracteres no permitidos.")
        if not self.validar_numero(telefono):
            raise InvalidPhoneNumberError("Número de teléfono inválido, debe tener exactamente 10 dígitos.")
        if not self.validar_email(email):
            raise InvalidEmailError("Formato de correo electrónico inválido.")

        self.nombre = nombre.strip()
        self.telefono = telefono
        self.email = email
        self.categoria = categoria.strip() if categoria.strip() else "Sin categoría"
        self.usuario_id = usuario_id

    def __str__(self):
        """
        Representación en cadena del contacto.

        Returns:
            str: Información formateada del contacto.
        """
        return f"{self.nombre} ({self.categoria}): {self.email}, {self.telefono}"

    @staticmethod
    def validar_numero(telefono: str) -> bool:
        """
        Valida que el número de teléfono tenga exactamente 10 dígitos.

        Args:
            telefono (str): Número de teléfono a validar.

        Returns:
            bool: True si es válido, False si no.
        """
        return telefono.isdigit() and len(telefono) == 10

    @staticmethod
    def validar_email(email: str, maximo_caracteres: int = 255) -> bool:
        """
        Valida el formato y longitud de un correo electrónico.

        Args:
            email (str): Correo electrónico a validar.
            maximo_caracteres (int, opcional): Longitud máxima permitida del correo. Por defecto es 255.

        Returns:
            bool: True si el email es válido, False si no.

        Raises:
            InvalidEmailTooLong: Si el correo excede el número máximo de caracteres.
        """
        if len(email) > maximo_caracteres:
            raise InvalidEmailTooLong(email, maximo_caracteres)
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None
