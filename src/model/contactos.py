import re
from src.model.excepciones import (InvalidEmailError, InvalidPhoneNumberError)

class Contacto:
    def __init__(self, nombre: str, telefono: str, email: str, categoria: str = "Sin categoría"):
        if not self.validate_phone(telefono):
            raise InvalidPhoneNumberError("Número de teléfono inválido, debe tener al menos 10 dígitos.")
        if not self.validate_email(email):
            raise InvalidEmailError("Formato de correo electrónico inválido.")

        self.nombre = nombre
        self.telefono = telefono
        self.email = email
        self.categoria = categoria if categoria else "Sin categoría"

    def __str__(self):
        return f"{self.nombre} ({self.categoria}): {self.email}, {self.telefono}"

    @staticmethod
    def validar_numero(telefono: str) -> bool:
        return isinstance(telefono, str) and telefono.isdigit() and len(telefono) == 10

    @staticmethod
    def validar_email(email: str) -> bool:
        pattern = r"^(?!.*\.{2})[\w\.-]{1,64}@[a-zA-Z\d.-]{1,185}\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

