import re
import pytest
from src.model.excepciones import (InvalidEmailError,ContactError, InvalidPasswordError, InvalidNameError)
                                    
from src.model.contactos import Contacto
from src.model.gestor_contactos import GestorDeContactos
from src.model.usuario import Usuario

def test_usuario_email_invalido():
    with pytest.raises(ValueError, match="Correo electrónico inválido"):
        Usuario("Juan", "correo_invalido", "contrasena123")

def test_usuario_iniciar_sesion_fallido():
    usuario = Usuario("Sara", "sara@correo.com", "password123")
    assert not usuario.iniciar_sesion("sara@correo.com", "wrongpassword")

def test_usuario_registro_con_password_vacia():
    with pytest.raises(InvalidPasswordError):
        Usuario("Juan", "juan@correo.com", "")

def test_usuario_login_email_mayusculas():
    usuario = Usuario("Sara", "sara@correo.com", "password123")
    assert usuario.iniciar_sesion("SARA@CORREO.COM", "password123")

def test_usuario_login_contraseña_incorrecta():
    usuario = Usuario("Sara", "sara@correo.com", "password123")
    assert not usuario.iniciar_sesion("sara@correo.com", "incorrecta456")

def test_usuario_registro_contraseña_muy_corta():
    with pytest.raises(InvalidPasswordError):
        Usuario("Juan", "juan@correo.com", "12345")

def test_usuario_login_email_no_registrado():
    usuario = Usuario("Carlos", "carlos@correo.com", "password123")
    assert not usuario.iniciar_sesion("no_existe@correo.com", "password123")

def test_usuario_registro_usuario_invalido():
    with pytest.raises(InvalidNameError):
        Usuario("J@c0b!", "jacob@correo.com", "password123")

def test_usuario_registro_email_vacio():
    with pytest.raises(InvalidEmailError):
        Usuario("Pedro", "", "password123")

def test_usuario_registro_contraseña_solo_espacios():
    with pytest.raises(InvalidPasswordError):
        Usuario("Juan", "juan@correo.com", "         ")

def test_usuario_login_email_vacio():
    usuario = Usuario("Ana", "ana@correo.com", "password123")
    assert not usuario.iniciar_sesion("", "password123")

def test_usuario_login_email_y_contraseña_incorrectos():
    usuario = Usuario("Elena", "elena@correo.com", "password123")
    assert not usuario.iniciar_sesion("emailIncorrecto@correo.com", "claveIncorrecta456")

def test_usuario_registro_nombre_vacio():
    with pytest.raises(InvalidNameError):
        Usuario("", "juan@correo.com", "password123")

def test_verificar_contraseña():
    usuario = Usuario("Ana", "ana@correo.com", "contraseñaSegura")
    assert usuario.verificar_contraseña("contraseñaSegura") is True
    assert usuario.verificar_contraseña("incorrecta") is False

def test_agregar_contacto_duplicado():
    usuario = Usuario("Luis", "luis@correo.com", "password123")
    contacto1 = Contacto("Pedro", "1234567890", "pedro@correo.com")
    contacto2 = Contacto("Pedro", "9876543210", "pedro@correo.com") 

    usuario.agregar_contacto(contacto1)
    with pytest.raises(ValueError):
        usuario.agregar_contacto(contacto2)



