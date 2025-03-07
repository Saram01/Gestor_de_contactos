import pytest
from src.model.excepciones import (InvalidPhoneNumberError, InvalidEmailError, 
                             ContactNotFoundError, DuplicateContactError, 
                             VCFExportError, VCFImportError, ContactError)
from src.model.contactos import Contacto
from src.model.gestor_contactos import GestorDeContactos
from src.model.usuario import Usuario

def test_agregar_contacto_exitoso():
    gestor = GestorDeContactos()
    contacto = Contacto("Luis", "3111111111", "luis@correo.com", "Amigo")
    gestor.agregar_contacto(contacto)
    assert len(gestor.contactos) == 1

def test_agregar_contacto_duplicado():
    gestor = GestorDeContactos()
    contacto = Contacto("Luis", "3111111111", "luis@correo.com", "Amigo")
    gestor.agregar_contacto(contacto)
    with pytest.raises(DuplicateContactError):
        gestor.agregar_contacto(contacto)

def test_editar_contacto_exitoso():
    gestor = GestorDeContactos()
    contacto = Contacto("Juan", "3107777777", "juan@correo.com", "Trabajo")
    gestor.agregar_contacto(contacto)
    gestor.editar_contacto("Juan", telefono="987654321")
    assert contacto.telefono == "987654321"

def test_editar_contacto_inexistente():
    gestor = GestorDeContactos()
    with pytest.raises(ContactNotFoundError):
        gestor.editar_contacto("Juan", telefono="987654321")

def test_editar_contacto_con_email_invalido():
    gestor = GestorDeContactos()
    contacto = Contacto("Pedro", "123456789", "pedro@example.com", "Trabajo")
    gestor.agregar_contacto(contacto)
    with pytest.raises(InvalidEmailError):
        gestor.editar_contacto("Pedro", email="pedroexample.com")

def test_filtrar_contactos_exitoso():
    gestor = GestorDeContactos()
    contacto1 = Contacto("Luis", "3111111111", "luis@correo.com", "Amigo")
    contacto2 = Contacto("Ana", "3222222222", "ana@correo.com", "Familia")
    gestor.agregar_contacto(contacto1)
    gestor.agregar_contacto(contacto2)
    assert len(gestor.filtrar_contacto("Amigo")) == 1
    assert len(gestor.filtrar_contacto("Familia")) == 1

def test_filtrar_contactos_categoria_inexistente():
    gestor = GestorDeContactos()
    assert len(gestor.filtrar_contacto("Trabajo")) == 0

def test_exportar_sin_permisos(mocker):
    gestor = GestorDeContactos()
    mocker.patch("builtins.open", side_effect=PermissionError)
    with pytest.raises(VCFExportError):
        gestor.exportar_vcf("contactos.vcf")

def test_importar_archivo_invalido(mocker):
    gestor = GestorDeContactos()
    mocker.patch("builtins.open", side_effect=FileNotFoundError)
    with pytest.raises(VCFImportError):
        gestor.importar_vcf("archivo_invalido.vcf")

def test_exportar_contactos_exitoso(mocker):
    gestor = GestorDeContactos()
    contacto = Contacto("Luis", "3111111111", "luis@example.com", "Amigo")
    gestor.agregar_contacto(contacto)
    mocker.patch("builtins.open", mocker.mock_open())
    gestor.exportar_vcf("contactos.vcf")