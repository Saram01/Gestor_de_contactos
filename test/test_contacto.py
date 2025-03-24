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
    contactos = ["Alice", "Bob", "Jaime"]
    with pytest.raises(ContactNotFoundError, match="El contacto 'Vanessa' no fue encontrado en la lista."):
        buscar_contacto(contactos, "Vanessa")


def test_email_invalido_muy_largo():
    with pytest.raises(InvalidEmailTooLong):
        validar_contacto("Laura", "9876543215", "lauraaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa@correo.com")
  
def test_crear_contacto_valido():
    contacto = Contacto("Luis", "1234567890", "luis@example.com", "Amigo")
    assert contacto.nombre == "Luis"
    assert contacto.telefono == "1234567890"
    assert contacto.email == "luis@example.com"
    assert contacto.categoria == "Amigo"

def test_telefono_demasiado_corto():
    with pytest.raises(InvalidPhoneNumberError, match="Número de teléfono inválido"):
        Contacto("Ana", "12345", "ana@example.com", "Familia")

def test_telefono_demasiado_largo():
    with pytest.raises(InvalidPhoneNumberError, match="Número de teléfono inválido"):
        Contacto("Carlos", "1234567890123456", "carlos@example.com", "Trabajo")

def test_telefono_no_numerico():
    with pytest.raises(InvalidPhoneNumberError, match="Número de teléfono inválido"):
        Contacto("Elena", "abcd123456", "elena@example.com", "Otro")

def test_email_invalido():
    with pytest.raises(InvalidEmailError, match="Correo electrónico inválido"):
        Contacto("Pedro", "1234567890", "correo-invalido", "Amigo")

def test_contacto_sin_categoria():
    contacto = Contacto("David", "9876543210", "david@example.com", None)
    assert contacto.categoria == "Sin categoría"

def test_email_muy_largo():
    email_largo = "a" * 64 + "@" + "b" * 185 + ".com"
    with pytest.raises(InvalidEmailError, match="Correo electrónico inválido"):
        Contacto("Laura", "9876543210", email_largo, "Trabajo")

def test_email_sin_dominio_valido():
    with pytest.raises(InvalidEmailError, match="Correo electrónico inválido"):
        Contacto("Sofia", "9876543210", "sofia@correo", "Familia")

def test_categoria_vacia():
    contacto = Contacto("Luis", "123456789", "luis@correo.com", "")
    assert contacto.categoria == ""

def test_nombre_con_caracteres_especiales():
    contacto = Contacto("Lu!s@", "123456789", "luis@correo.com", "Amigo")
    assert contacto.nombre == "Lu!s@"

def test_email_sin_dominio_valido():
    with pytest.raises(InvalidEmailError):
        validar_contacto("Sofia", "9876543210", "sofia@correo", "Amigo")

def test_nombre_solo_espacios():
    with pytest.raises(ContactError):
        validar_contacto("   ", "9876543210", "espacios@correo.com")

def test_contacto_sin_categoria():
    contacto = Contacto("David", "9876543210", "david@correo.com", None)
    assert contacto.categoria is None
