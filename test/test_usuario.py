import pytest
from src.model.excepciones import (InvalidPhoneNumberError, InvalidEmailError, 
                             ContactNotFoundError, DuplicateContactError, 
                             VCFExportError, VCFImportError, ContactError)
from src.model.contactos import Contacto
from src.model.gestor_contactos import GestorDeContactos
from src.model.usuario import Usuario

def test_usuario_registro_con_email_invalido():
    with pytest.raises(InvalidEmailError):
        Usuario("Sara", "saracorreo.com", "password123")

def test_usuario_iniciar_sesion_fallido():
    usuario = Usuario("Sara", "sara@correo.com", "password123")
    assert not usuario.iniciar_sesion("sara@correo.com", "wrongpassword")

def test_usuario_registro_con_password_vacia():
    with pytest.raises(ContactError):
        Usuario("Sara", "sara@correo.com", "")

def test_usuario_login_email_mayusculas():
    usuario = Usuario("Sara", "sara@correo.com", "password123")
    assert usuario.iniciar_sesion("SARA@CORREO.COM", "password123")

def test_usuario_login_contraseña_incorrecta():
    usuario = Usuario("Sara", "sara@correo.com", "password123")
    assert not usuario.iniciar_sesion("sara@correo.com", "incorrecta456")

