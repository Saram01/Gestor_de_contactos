import bcrypt
import re
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.model.base import Base
from src.model.excepciones import (
    InvalidNameError,
    InvalidEmailError,
    InvalidPasswordError,
)

class Usuario(Base):
    """
    Representa un usuario que puede registrarse y manejar contactos.
    """
    __tablename__ = 'usuario'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_usuario = Column(String(30), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    contrasena = Column(String(100), nullable=False)
    contactos = relationship("Contacto", back_populates="usuario")

    def __init__(self, nombre_usuario: str, email: str, password: str):
        if not self.validar_nombre(nombre_usuario):
            raise InvalidNameError("Nombre de usuario inválido.")
        if not self.validar_email(email):
            raise InvalidEmailError("Email inválido.")
        if not self.validar_password(password):
            raise InvalidPasswordError("Contraseña insegura.")
        self.nombre_usuario = nombre_usuario
        self.email = email
        self.contrasena = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def verificar_contraseña(self, contraseña: str) -> bool:
        return bcrypt.checkpw(contraseña.encode(), self.contrasena.encode())

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

    def __repr__(self):
        return f"<Usuario(nombre_usuario={self.nombre_usuario}, email={self.email})>"
