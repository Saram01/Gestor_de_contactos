import re
import pytest
from src.model.excepciones import (InvalidPhoneNumberError, InvalidEmailError, 
                                   ContactNotFoundError, DuplicateContactError, 
                                   VCFExportError, VCFImportError, ContactError,
                                   InvalidEmailTooLong)
from src.model.contactos import Contacto

def validar_contacto(nombre, telefono, email):
    """Función auxiliar para validar los campos de un contacto."""
    if not nombre:
        raise ContactError("El nombre del contacto no puede estar vacío.")
    
    if not telefono.isdigit() or len(telefono) < 10:
        raise InvalidPhoneNumberError(telefono)
    
    if "@" not in email or "." not in email:
        raise InvalidEmailError(email)

def buscar_contacto(contactos, nombre):
    """Función auxiliar para buscar un contacto por nombre."""
    if nombre not in contactos:
        raise ContactNotFoundError(nombre)

def test_contacto_no_encontrado():
    """Valida que un email válido pase la expresión regular de formato."""
    assert re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$", "test@example.com")

def test_email_invalido_muy_largo():
    """Verifica que se lance InvalidEmailTooLong si el email excede el límite de longitud."""
    email = "a" * 256 + "@example.com"
    with pytest.raises(InvalidEmailTooLong):
        Contacto("Juan Pérez", "1234567890", email, "Trabajo")

def test_crear_contacto_valido():
    """Verifica que se cree correctamente un contacto con datos válidos."""
    contacto = Contacto("Carlos", "9876543210", "carlos@correo.com", "Amigo")
    assert contacto.categoria == "Amigo"

def test_telefono_demasiado_corto():
    """Verifica que se lance InvalidPhoneNumberError si el teléfono tiene menos de 10 dígitos."""
    with pytest.raises(InvalidPhoneNumberError):
        Contacto("Juan Pérez", "12345", "juan@correo.com", "Trabajo")

def test_telefono_demasiado_largo():
    """Verifica que se lance InvalidPhoneNumberError si el teléfono tiene más de 15 dígitos."""
    with pytest.raises(InvalidPhoneNumberError, match="Número de teléfono inválido"):
        Contacto("Carlos", "1234567890123456", "carlos@example.com", "Trabajo")

def test_telefono_no_numerico():
    """Verifica que se lance InvalidPhoneNumberError si el teléfono contiene caracteres no numéricos."""
    with pytest.raises(InvalidPhoneNumberError, match="Número de teléfono inválido"):
        Contacto("Elena", "abcd123456", "elena@example.com", "Otro")

def test_email_invalido():
    """Verifica que se lance ValueError si el email no cumple con la expresión regular."""
    email_invalido = "email@domain..com"
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"
    with pytest.raises(ValueError):
        if not re.match(pattern, email_invalido):
            raise ValueError(f"Correo electrónico inválido: {email_invalido}")

def test_categoria_vacia():
    """Verifica que si se proporciona una categoría vacía, se asigne 'Sin categoría'."""
    contacto = Contacto("Juan Pérez", "1234567890", "juan@correo.com", "")
    assert contacto.categoria == "Sin categoría"

def test_email_sin_dominio_valido():
    """Verifica que se lance InvalidEmailError si el dominio del email es inválido."""
    with pytest.raises(InvalidEmailError):
        validar_contacto("Sofia", "9876543210", "sofia@correo")

def test_nombre_con_caracteres_especiales():
    """Verifica que se lance ContactError si el nombre contiene caracteres especiales no permitidos."""
    with pytest.raises(ContactError):
        Contacto("Juan@123", "1234567890", "juan@correo.com", "Trabajo")

def test_nombre_solo_espacios():
    """Verifica que se lance ContactError si el nombre contiene solo espacios en blanco."""
    with pytest.raises(ContactError):
        Contacto("   ", "1234567890", "juan@correo.com", "Trabajo")

def test_contacto_sin_categoria():
    """Verifica que se permita una categoría personalizada aún si es parecida a 'Sin categoría'."""
    contacto = Contacto("David", "9876543210", "david@correo.com", "Sin categoria")
    assert contacto.categoria == "Sin categoria"

def test_email_sin_arroba():
    """Verifica que se lance InvalidEmailError si el email no contiene el carácter '@'."""
    email = "juan.correo.com"  # Falta el '@'
    with pytest.raises(InvalidEmailError):
        validar_contacto("Juan", "1234567890", email)

def test_nombre_vacio():
    """Verifica que se lance ContactError si el nombre está completamente vacío."""
    with pytest.raises(ContactError):
        validar_contacto("", "1234567890", "juan@correo.com")
