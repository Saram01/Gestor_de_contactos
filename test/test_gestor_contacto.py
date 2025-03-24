import os
import pytest
from src.model.excepciones import (InvalidPhoneNumberError, InvalidEmailError, 
                             ContactNotFoundError, DuplicateContactError, 
                             VCFExportError, VCFImportError, ContactError)
from src.model.contactos import Contacto
from src.model.gestor_contactos import GestorDeContactos
from src.model.usuario import Usuario

def test_agregar_contacto_exitoso():
    gestor = GestorDeContactos()
    contacto = Contacto("Juan", "1234567890", "juan@correo.com", "Trabajo")
    gestor.agregar_contacto(contacto)
    assert contacto in gestor.contactos  

def test_agregar_contacto_duplicado():
    usuario = Usuario("Luis", "luis@correo.com", "password123")
    contacto1 = Contacto("Pedro", "1234567890", "pedro@correo.com")
    contacto2 = Contacto("Pedro", "9876543210", "pedro@correo.com")
    usuario.agregar_contacto(contacto1)
    with pytest.raises(ValueError):
        usuario.agregar_contacto(contacto2)


def test_editar_contacto_exitoso():
    gestor = GestorDeContactos()
    contacto = Contacto("Juan", "1234567890", "juan@correo.com", "Trabajo")
    gestor.agregar_contacto(contacto)
    gestor.editar_contacto("Juan", telefono="9876543210")
    assert contacto.telefono == "9876543210"

def test_editar_contacto_inexistente():
    gestor = GestorDeContactos()
    with pytest.raises(ContactNotFoundError):
        gestor.editar_contacto("Juan", telefono="987654321")

def test_editar_contacto_con_email_invalido():
    gestor = GestorDeContactos()
    contacto = Contacto("Pedro", "1234567890", "pedro@correo.com", "Trabajo")
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


def test_agregar_contacto_sin_categoria():
    gestor = GestorDeContactos()
    contacto = Contacto("Sofia", "9876543210", "sofia@correo.com")
    gestor.agregar_contacto(contacto)
    assert contacto.categoria == "Sin categoría"

def test_buscar_contacto_case_sensitive():
    gestor = GestorDeContactos()
    contacto = Contacto("Carlos", "9876543210", "carlos@correo.com", "Familia")
    gestor.agregar_contacto(contacto)
    resultado = gestor.buscar_contacto("carlos")
    assert len(resultado) == 1 and resultado[0] == contacto

def test_exportar_contactos_vacio():
    gestor = GestorDeContactos()
    with pytest.raises(VCFExportError):
        gestor.exportar_a_vcf("contactos_vacios.vcf")

def test_importar_contactos_vcf_vacio():
    gestor = GestorDeContactos()
    with pytest.raises(VCFImportError):
        gestor.importar_desde_vcf("vacio.vcf")

def test_editar_contacto_nombre_vacio():
    gestor = GestorDeContactos()
    contacto = Contacto("Elena", "9876543210", "elena@correo.com", "Amigo")
    gestor.agregar_contacto(contacto)
    with pytest.raises(ContactNotFoundError):
        gestor.editar_contacto("", telefono="1122334455")

def test_agregar_contacto_telefono_con_espacios():
    gestor = GestorDeContactos()
    with pytest.raises(InvalidPhoneNumberError):
        gestor.agregar_contacto(Contacto("Fernando", "98 76 54 32 10", "fernando@correo.com", "Trabajo"))

def test_eliminar_contacto_por_numero():
    gestor = GestorDeContactos()
    contacto = Contacto("David", "9876543210", "david@correo.com", "Trabajo")
    gestor.agregar_contacto(contacto)
    gestor.eliminar_contacto("david@correo.com")
    assert contacto not in gestor.contactos

def test_agregar_contacto_email_caracteres_invalidos():
    gestor = GestorDeContactos()
    with pytest.raises(InvalidEmailError):
        gestor.agregar_contacto(Contacto("Marina", "9876543210", "marina@@correo..com", "Familia"))

def test_editar_contacto_eliminar_categoria():
    gestor = GestorDeContactos()
    contacto = Contacto("Andrés", "1234567890", "andres@correo.com", "Trabajo")
    gestor.agregar_contacto(contacto)
    gestor.editar_contacto("Andrés", categoria="")
    assert contacto.categoria == ""

def test_agregar_contacto_mismo_nombre_diferente_datos():
    gestor = GestorDeContactos()
    contacto1 = Contacto("Daniel", "1234567890", "daniel@correo.com", "Trabajo")
    contacto2 = Contacto("Daniel", "0987654321", "daniel.otro@correo.com", "Familia")
    gestor.agregar_contacto(contacto1)
    gestor.agregar_contacto(contacto2)
    assert len(gestor.contactos) == 2

def test_exportar_contactos_error():
    gestor = GestorDeContactos()
    with pytest.raises(VCFExportError):
        gestor.exportar_a_vcf("/ruta/invalida/contactos.vcf")

def test_importar_contactos_vcf_corrupto():
    gestor = GestorDeContactos()
    with pytest.raises(VCFImportError):
        gestor.importar_desde_vcf("/ruta/invalida/contactos_corruptos.vcf")

def test_buscar_contacto_telefono_invalido():
    gestor = GestorDeContactos()
    with pytest.raises(InvalidPhoneNumberError):
        gestor.agregar_contacto(Contacto("Luis", "abcdef1234", "luis@correo.com", "Amigo"))

def test_agregar_contacto_nombre_excesivamente_largo():
    gestor = GestorDeContactos()
    nombre_largo = "A" * 201 
    with pytest.raises(ContactError) as excinfo:
        gestor.agregar_contacto(Contacto(nombre_largo, "9876543210", "contacto@correo.com", "Amigo"))
    assert str(excinfo.value) == "El nombre no puede exceder los 200 caracteres."

def test_agregar_contacto_categoria_muy_larga():
    gestor = GestorDeContactos()
    with pytest.raises(ContactError):
        gestor.agregar_contacto(Contacto("Marta", "9876543210", "marta@correo.com", "A" * 101))
