import pytest
from src.model.excepciones import (InvalidPhoneNumberError, InvalidEmailError, 
                             ContactNotFoundError, DuplicateContactError, 
                             VCFExportError, VCFImportError, ContactError)
from src.model.contactos import Contacto
from src.model.gestor_contactos import GestorDeContactos
from src.model.usuario import Usuario

def test_agregar_contacto_exitoso():
    gestor = GestorDeContactos()
    contacto = Contacto("Luis", "123456789", "luis@correo.com", "Amigo")
    gestor.agregar_contacto(contacto)
    assert len(gestor.contactos) == 1

def test_agregar_contacto_duplicado():
    gestor = GestorDeContactos()
    contacto = Contacto("Luis", "123456789", "luis@correo.com", "Amigo")
    gestor.agregar_contacto(contacto)
    with pytest.raises(DuplicateContactError):
        gestor.agregar_contacto(contacto)

def test_editar_contacto_exitoso():
    gestor = GestorDeContactos()
    contacto = Contacto("Juan", "123456789", "juan@correo.com", "Trabajo")
    gestor.agregar_contacto(contacto)
    gestor.editar_contacto("Juan", telefono="987654321")
    assert contacto.telefono == "987654321"

def test_editar_contacto_inexistente():
    gestor = GestorDeContactos()
    with pytest.raises(ContactNotFoundError):
        gestor.editar_contacto("Juan", telefono="987654321")

def test_editar_contacto_con_email_invalido():
    gestor = GestorDeContactos()
    contacto = Contacto("Pedro", "123456789", "pedro@correo.com", "Trabajo")
    gestor.agregar_contacto(contacto)
    with pytest.raises(InvalidEmailError):
        gestor.editar_contacto("Pedro", email="pedrocorreo.com")

def test_filtrar_contacto_no_existente():
    gestor = GestorDeContactos()
    assert len(gestor.filtrar_contacto("Trabajo")) == 0

def test_eliminar_contacto_con_nombre_vacio():
    gestor = GestorDeContactos()
    with pytest.raises(ContactError):
        gestor.eliminar_contacto("")