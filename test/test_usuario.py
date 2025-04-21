import re
import pytest
from src.model.excepciones import (InvalidEmailError, ContactError, InvalidPasswordError, InvalidNameError)
from src.model.contactos import Contacto
from src.model.gestor_contactos import GestorDeContactos
from src.model.usuario import Usuario

def test_usuario_email_invalido():
    """Verifica que se lance ValueError al registrar un usuario con un email inválido."""
    with pytest.raises(ValueError, match="Correo electrónico inválido"):
        Usuario("Juan", "correo_invalido", "contrasena123")

def test_usuario_iniciar_sesion_fallido():
    """Prueba que el inicio de sesión falle con contraseña incorrecta."""
    usuario = Usuario("Sara", "sara@correo.com", "password123")
    assert not usuario.iniciar_sesion("sara@correo.com", "wrongpassword")

def test_usuario_registro_con_password_vacia():
    """Verifica que se lance InvalidPasswordError al registrar con contraseña vacía."""
    with pytest.raises(InvalidPasswordError):
        Usuario("Juan", "juan@correo.com", "")

def test_usuario_login_email_mayusculas():
    """Prueba que el login funcione aunque el email tenga mayúsculas."""
    usuario = Usuario("Sara", "sara@correo.com", "password123")
    assert usuario.iniciar_sesion("SARA@CORREO.COM", "password123")

def test_usuario_login_contraseña_incorrecta():
    """Verifica que el login falle si la contraseña es incorrecta."""
    usuario = Usuario("Sara", "sara@correo.com", "password123")
    assert not usuario.iniciar_sesion("sara@correo.com", "incorrecta456")

def test_usuario_registro_contraseña_muy_corta():
    """Verifica que se lance InvalidPasswordError si la contraseña es demasiado corta."""
    with pytest.raises(InvalidPasswordError):
        Usuario("Juan", "juan@correo.com", "12345")

def test_usuario_login_email_no_registrado():
    """Prueba que no se pueda iniciar sesión con un email no registrado."""
    usuario = Usuario("Carlos", "carlos@correo.com", "password123")
    assert not usuario.iniciar_sesion("no_existe@correo.com", "password123")

def test_usuario_registro_usuario_invalido():
    """Verifica que se lance InvalidNameError si el nombre contiene caracteres inválidos."""
    with pytest.raises(InvalidNameError):
        Usuario("J@c0b!", "jacob@correo.com", "password123")

def test_usuario_registro_email_vacio():
    """Verifica que se lance InvalidEmailError al registrar con email vacío."""
    with pytest.raises(InvalidEmailError):
        Usuario("Pedro", "", "password123")

def test_usuario_registro_contraseña_solo_espacios():
    """Verifica que se lance InvalidPasswordError si la contraseña contiene solo espacios."""
    with pytest.raises(InvalidPasswordError):
        Usuario("Juan", "juan@correo.com", "         ")

def test_usuario_login_email_vacio():
    """Prueba que el login falle si el email está vacío."""
    usuario = Usuario("Ana", "ana@correo.com", "password123")
    assert not usuario.iniciar_sesion("", "password123")

def test_usuario_login_email_y_contraseña_incorrectos():
    """Verifica que no se pueda iniciar sesión con email y contraseña incorrectos."""
    usuario = Usuario("Elena", "elena@correo.com", "password123")
    assert not usuario.iniciar_sesion("emailIncorrecto@correo.com", "claveIncorrecta456")

def test_usuario_registro_nombre_vacio():
    """Verifica que se lance InvalidNameError si el nombre está vacío al registrar."""
    with pytest.raises(InvalidNameError):
        Usuario("", "juan@correo.com", "password123")

def test_verificar_contraseña():
    """Prueba el método verificar_contraseña con contraseña correcta e incorrecta."""
    usuario = Usuario("Ana", "ana@correo.com", "contraseñaSegura")
    assert usuario.verificar_contraseña("contraseñaSegura") is True
    assert usuario.verificar_contraseña("incorrecta") is False

def test_agregar_contacto_duplicado():
    """Verifica que no se pueda agregar un contacto duplicado con el mismo email."""
    usuario = Usuario("Luis", "luis@correo.com", "password123")
    contacto1 = Contacto("Pedro", "1234567890", "pedro@correo.com")
    contacto2 = Contacto("Pedro", "9876543210", "pedro@correo.com") 

    usuario.agregar_contacto(contacto1)
    with pytest.raises(ValueError):
        usuario.agregar_contacto(contacto2)
