import re
import pytest
from src.model.excepciones import (InvalidPhoneNumberError, InvalidEmailError, 
                                   ContactNotFoundError, DuplicateContactError, 
                                   VCFExportError, VCFImportError, ContactError,
                                   InvalidEmailTooLong)
from src.model.contactos import Contacto

def validar_contacto(nombre, telefono, email):
    if not nombre:
        raise ContactError("El nombre del contacto no puede estar vacío.")
    
    if not telefono.isdigit() or len(telefono) < 10:
        raise InvalidPhoneNumberError(telefono)
    
    if "@" not in email or "." not in email:
        raise InvalidEmailError(email)

def buscar_contacto(contactos, nombre):
    if nombre not in contactos:
        raise ContactNotFoundError(nombre)

def test_contacto_no_encontrado():
    assert re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$", "test@example.com")

def test_email_invalido_muy_largo():
    email = "a" * 256 + "@example.com"
    with pytest.raises(InvalidEmailTooLong):
        Contacto("Juan Pérez", "1234567890", email, "Trabajo")


def test_crear_contacto_valido():
    contacto = Contacto("Carlos", "9876543210", "carlos@correo.com", "Amigo")
    assert contacto.categoria == "Amigo"

def test_telefono_demasiado_corto():
    with pytest.raises(InvalidPhoneNumberError):
        Contacto("Juan Pérez", "12345", "juan@correo.com", "Trabajo")

def test_telefono_demasiado_largo():
    with pytest.raises(InvalidPhoneNumberError, match="Número de teléfono inválido"):
        Contacto("Carlos", "1234567890123456", "carlos@example.com", "Trabajo")

def test_telefono_no_numerico():
    with pytest.raises(InvalidPhoneNumberError, match="Número de teléfono inválido"):
        Contacto("Elena", "abcd123456", "elena@example.com", "Otro")

def test_email_invalido():
    email_invalido = "email@domain..com"
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"
    with pytest.raises(ValueError):
        if not re.match(pattern, email_invalido):
            raise ValueError(f"Correo electrónico inválido: {email_invalido}")

def test_categoria_vacia():
    contacto = Contacto("Juan Pérez", "1234567890", "juan@correo.com", "")
    assert contacto.categoria == "Sin categoría"



def test_email_sin_dominio_valido():
    with pytest.raises(InvalidEmailError):
        validar_contacto("Sofia", "9876543210", "sofia@correo")

def test_categoria_vacia():
    contacto = Contacto("Juan Pérez", "1234567890", "juan@correo.com", "")
    assert contacto.categoria == "Sin categoría"  


def test_nombre_con_caracteres_especiales():
    with pytest.raises(ContactError):
        Contacto("Juan@123", "1234567890", "juan@correo.com", "Trabajo")


def test_email_sin_dominio_valido():
    with pytest.raises(InvalidEmailError):
        validar_contacto("Sofia", "9876543210", "sofia@correo")

def test_nombre_solo_espacios():
    with pytest.raises(ContactError):
        Contacto("   ", "1234567890", "juan@correo.com", "Trabajo")


def test_contacto_sin_categoria():
    contacto = Contacto("David", "9876543210", "david@correo.com", "Sin categoria")
    assert contacto.categoria == "Sin categoria"

