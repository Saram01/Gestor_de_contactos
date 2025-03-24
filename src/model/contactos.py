import re
from src.model.excepciones import (InvalidEmailError, InvalidPhoneNumberError, InvalidEmailTooLong, ContactError)

class Contacto:
    def __init__(self, nombre: str, telefono: str, email: str, categoria: str = "Sin categoría"):
        if not nombre.strip():
            raise ContactError("El nombre no puede estar vacío o compuesto solo por espacios.")
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$", nombre):
            raise ContactError("El nombre contiene caracteres no permitidos.")
        if not self.validar_numero(telefono):
            raise InvalidPhoneNumberError("Número de teléfono inválido, debe tener al menos 10 dígitos.")
        if not self.validar_email(email):
            raise InvalidEmailError("Formato de correo electrónico inválido.")
        self.nombre = nombre.strip()
        self.telefono = telefono
        self.email = email
        self.categoria = categoria.strip() if categoria.strip() else "Sin categoría"


    def __str__(self):
        return f"{self.nombre} ({self.categoria}): {self.email}, {self.telefono}"

    @staticmethod
    def validar_numero(telefono: str) -> bool:
        return telefono.isdigit() and len(telefono) == 10

    @staticmethod
    def validar_email(email: str, maximo_caracteres: int = 255) -> bool:
        if len(email) > maximo_caracteres:
            raise InvalidEmailTooLong(email, maximo_caracteres)
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

