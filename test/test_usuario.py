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

# parte de Jenn x3 xd
def test_usuario_registro_contraseña_muy_corta():
    with pytest.raises(ContactError):
        Usuario("Carlos", "carlos@correo.com", "123")
#2
def test_usuario_login_email_no_registrado():
    usuario = Usuario("Carlos", "carlos@correo.com", "password123")
    assert not usuario.iniciar_sesion("no_existe@correo.com", "password123")
#4
def test_agregar_contacto_categoria_muy_larga():
    gestor = GestorDeContactos()
    with pytest.raises(ContactError):
        gestor.agregar_contacto(Contacto("Marta", "9876543210", "marta@correo.com", "A" * 101))
#5
def test_usuario_registro_email_vacio():
    with pytest.raises(InvalidEmailError):
        Usuario("Pedro", "", "password123")
#6
def test_usuario_registro_contraseña_solo_espacios():
    with pytest.raises(ContactError):
        Usuario("Ana", "ana@correo.com", "     ")
#7
def test_usuario_login_email_vacio():
    usuario = Usuario("Ana", "ana@correo.com", "password123")
    assert not usuario.iniciar_sesion("", "password123")
#8
def test_usuario_login_email_y_contraseña_incorrectos():
    usuario = Usuario("Elena", "elena@correo.com", "password123")
    assert not usuario.iniciar_sesion("emailIncorrecto@correo.com", "claveIncorrecta456")
#9
def test_usuario_registro_nombre_vacio():
    with pytest.raises(ContactError):
        Usuario("", "usuario@correo.com", "password123")
