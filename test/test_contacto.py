import pytest
import re
from src.model.excepciones import (InvalidPhoneNumberError, InvalidEmailError, 
                                   ContactNotFoundError, DuplicateContactError, 
                                   VCFExportError, VCFImportError, ContactError)
from src.model.contactos import Contacto
from src.model.gestor_contactos import GestorDeContactos
from src.model.usuario import Usuario

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


    
