import pytest
from src.model.excepciones import (InvalidPhoneNumberError, InvalidEmailError, 
                             ContactNotFoundError, DuplicateContactError, 
                             VCFExportError, VCFImportError, ContactError)
from src.model.contactos import Contacto
from src.model.gestor_contactos import GestorDeContactos
from src.model.usuario import Usuario

def test_registro_usuario_exitoso():
    usuario = Usuario("Sara", "sara@example.com", "password123")
    assert usuario.nombre == "Sara"
    assert usuario.email == "sara@example.com"

def test_registro_email_invalido():
    with pytest.raises(InvalidEmailError):
        Usuario("Sara", "saraexample.com", "password123")

def test_iniciar_sesion_exitoso():
    usuario = Usuario("Sara", "sara@example.com", "password123")
    assert usuario.iniciar_sesion("sara@example.com", "password123")

def test_iniciar_sesion_fallido():
    usuario = Usuario("Sara", "sara@example.com", "password123")
    assert not usuario.iniciar_sesion("sara@example.com", "wrongpassword")

def test_usuario_agregar_contacto():
    usuario = Usuario("Sara", "sara@example.com", "password123")
    contacto = Contacto("Luis", "123456789", "luis@example.com", "Amigo")
    usuario.contactos.append(contacto)
    assert len(usuario.contactos) == 1

