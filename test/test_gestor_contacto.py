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

#parte de Jenn x2 xd
def test_agregar_contacto_sin_categoria():
    gestor = GestorDeContactos()
    contacto = Contacto("Sofia", "9876543210", "sofia@correo.com", "")
    gestor.agregar_contacto(contacto)
    assert contacto.categoria == ""
#2
def test_buscar_contacto_case_sensitive():
    gestor = GestorDeContactos()
    contacto = Contacto("Carlos", "9876543210", "carlos@correo.com", "Familia")
    gestor.agregar_contacto(contacto)
    resultado = gestor.buscar_contacto("carlos")  # Diferente a "Carlos"
    assert resultado is None or len(resultado) == 0
#3
def test_exportar_contactos_vacio():
    gestor = GestorDeContactos()
    with pytest.raises(VCFExportError):
        gestor.exportar_a_vcf("contactos_vacios.vcf")
#4
def test_importar_contactos_vcf_vacio():
    gestor = GestorDeContactos()
    with pytest.raises(VCFImportError):
        gestor.importar_desde_vcf("vacio.vcf")
#5
def test_editar_contacto_nombre_vacio():
    gestor = GestorDeContactos()
    contacto = Contacto("Elena", "9876543210", "elena@correo.com", "Amigo")
    gestor.agregar_contacto(contacto)
    with pytest.raises(ContactError):
        gestor.editar_contacto("", telefono="1122334455")
#6
def test_agregar_contacto_telefono_con_espacios():
    gestor = GestorDeContactos()
    with pytest.raises(InvalidPhoneNumberError):
        gestor.agregar_contacto(Contacto("Fernando", "98 76 54 32 10", "fernando@correo.com", "Trabajo"))
#7
def test_eliminar_contacto_por_numero():
    gestor = GestorDeContactos()
    contacto = Contacto("David", "9876543210", "david@correo.com", "Trabajo")
    gestor.agregar_contacto(contacto)
    with pytest.raises(ContactError):
        gestor.eliminar_contacto("9876543210")  # Pasar el número en vez del nombre
#8
def test_agregar_contacto_email_caracteres_invalidos():
    gestor = GestorDeContactos()
    with pytest.raises(InvalidEmailError):
        gestor.agregar_contacto(Contacto("Marina", "9876543210", "marina@@correo..com", "Familia"))
#9
def test_editar_contacto_eliminar_categoria():
    gestor = GestorDeContactos()
    contacto = Contacto("Andrés", "1234567890", "andres@correo.com", "Trabajo")
    gestor.agregar_contacto(contacto)
    gestor.editar_contacto("Andrés", categoria="")
    assert contacto.categoria == ""
