import os
import pytest
from src.model.excepciones import (InvalidPhoneNumberError, InvalidEmailError, 
                             ContactNotFoundError, DuplicateContactError, 
                             VCFExportError, VCFImportError, ContactError)
from src.model.contactos import Contacto
from src.model.gestor_contactos import GestorDeContactos
from src.model.usuario import Usuario

def test_agregar_contacto_exitoso():
    """Verifica que se pueda agregar un contacto exitosamente."""
    gestor = GestorDeContactos()
    contacto = Contacto("Juan", "1234567890", "juan@correo.com", "Trabajo")
    gestor.agregar_contacto(contacto)
    assert contacto in gestor.contactos  

def test_agregar_contacto_duplicado():
    """Verifica que no se puedan agregar dos contactos con el mismo email."""
    usuario = Usuario("Luis", "luis@correo.com", "password123")
    contacto1 = Contacto("Pedro", "1234567890", "pedro@correo.com")
    contacto2 = Contacto("Pedro", "9876543210", "pedro@correo.com")
    usuario.agregar_contacto(contacto1)
    with pytest.raises(ValueError):
        usuario.agregar_contacto(contacto2)

def test_editar_contacto_exitoso():
    """Prueba que se pueda editar un contacto correctamente."""
    gestor = GestorDeContactos()
    contacto = Contacto("Juan", "1234567890", "juan@correo.com", "Trabajo")
    gestor.agregar_contacto(contacto)
    gestor.editar_contacto("Juan", telefono="9876543210")
    assert contacto.telefono == "9876543210"

def test_editar_contacto_inexistente():
    """Verifica que lanzar excepción si se intenta editar un contacto inexistente."""
    gestor = GestorDeContactos()
    with pytest.raises(ContactNotFoundError):
        gestor.editar_contacto("Juan", telefono="987654321")

def test_editar_contacto_con_email_invalido():
    """Verifica que se lance InvalidEmailError si se asigna un email inválido al editar."""
    gestor = GestorDeContactos()
    contacto = Contacto("Pedro", "1234567890", "pedro@correo.com", "Trabajo")
    gestor.agregar_contacto(contacto)
    with pytest.raises(InvalidEmailError):
        gestor.editar_contacto("Pedro", email="pedrocorreo.com")

def test_filtrar_contacto_no_existente():
    """Verifica que filtrar por categoría inexistente retorne lista vacía."""
    gestor = GestorDeContactos()
    assert len(gestor.filtrar_contacto("Trabajo")) == 0

def test_eliminar_contacto_con_nombre_vacio():
    """Verifica que se lance ContactError al intentar eliminar un contacto con nombre vacío."""
    gestor = GestorDeContactos()
    with pytest.raises(ContactError):
        gestor.eliminar_contacto("")

def test_agregar_contacto_sin_categoria():
    """Verifica que un contacto sin categoría se asigne con 'Sin categoría' por defecto."""
    gestor = GestorDeContactos()
    contacto = Contacto("Sofia", "9876543210", "sofia@correo.com")
    gestor.agregar_contacto(contacto)
    assert contacto.categoria == "Sin categoría"

def test_buscar_contacto_case_sensitive():
    """Prueba la búsqueda de contacto ignorando mayúsculas/minúsculas."""
    gestor = GestorDeContactos()
    contacto = Contacto("Carlos", "9876543210", "carlos@correo.com", "Familia")
    gestor.agregar_contacto(contacto)
    resultado = gestor.buscar_contacto("carlos")
    assert len(resultado) == 1 and resultado[0] == contacto

def test_exportar_contactos_vacio():
    """Verifica que se lance VCFExportError al exportar si no hay contactos."""
    gestor = GestorDeContactos()
    with pytest.raises(VCFExportError):
        gestor.exportar_a_vcf("contactos_vacios.vcf")

def test_importar_contactos_vcf_vacio():
    """Verifica que se lance VCFImportError al importar desde un archivo VCF vacío."""
    gestor = GestorDeContactos()
    with pytest.raises(VCFImportError):
        gestor.importar_desde_vcf("vacio.vcf")

def test_editar_contacto_nombre_vacio():
    """Verifica que se lance ContactNotFoundError si se intenta editar un contacto sin nombre."""
    gestor = GestorDeContactos()
    contacto = Contacto("Elena", "9876543210", "elena@correo.com", "Amigo")
    gestor.agregar_contacto(contacto)
    with pytest.raises(ContactNotFoundError):
        gestor.editar_contacto("", telefono="1122334455")

def test_agregar_contacto_telefono_con_espacios():
    """Verifica que se lance InvalidPhoneNumberError si el teléfono tiene espacios."""
    gestor = GestorDeContactos()
    with pytest.raises(InvalidPhoneNumberError):
        gestor.agregar_contacto(Contacto("Fernando", "98 76 54 32 10", "fernando@correo.com", "Trabajo"))

def test_eliminar_contacto_por_numero():
    """Prueba que se pueda eliminar un contacto por su email."""
    gestor = GestorDeContactos()
    contacto = Contacto("David", "9876543210", "david@correo.com", "Trabajo")
    gestor.agregar_contacto(contacto)
    gestor.eliminar_contacto("david@correo.com")
    assert contacto not in gestor.contactos

def test_agregar_contacto_email_caracteres_invalidos():
    """Verifica que se lance InvalidEmailError si el email tiene caracteres inválidos."""
    gestor = GestorDeContactos()
    with pytest.raises(InvalidEmailError):
        gestor.agregar_contacto(Contacto("Marina", "9876543210", "marina@@correo..com", "Familia"))

def test_editar_contacto_eliminar_categoria():
    """Verifica que se pueda eliminar la categoría de un contacto asignándole una cadena vacía."""
    gestor = GestorDeContactos()
    contacto = Contacto("Andrés", "1234567890", "andres@correo.com", "Trabajo")
    gestor.agregar_contacto(contacto)
    gestor.editar_contacto("Andrés", categoria="")
    assert contacto.categoria == ""

def test_agregar_contacto_mismo_nombre_diferente_datos():
    """Prueba que se puedan agregar contactos con el mismo nombre si los datos son diferentes."""
    gestor = GestorDeContactos()
    contacto1 = Contacto("Daniel", "1234567890", "daniel@correo.com", "Trabajo")
    contacto2 = Contacto("Daniel", "0987654321", "daniel.otro@correo.com", "Familia")
    gestor.agregar_contacto(contacto1)
    gestor.agregar_contacto(contacto2)
    assert len(gestor.contactos) == 2

def test_exportar_contactos_error():
    """Verifica que se lance VCFExportError si la ruta de exportación es inválida."""
    gestor = GestorDeContactos()
    with pytest.raises(VCFExportError):
        gestor.exportar_a_vcf("/ruta/invalida/contactos.vcf")

def test_importar_contactos_vcf_corrupto():
    """Verifica que se lance VCFImportError si el archivo VCF está corrupto o es ilegible."""
    gestor = GestorDeContactos()
    with pytest.raises(VCFImportError):
        gestor.importar_desde_vcf("/ruta/invalida/contactos_corruptos.vcf")

def test_buscar_contacto_telefono_invalido():
    """Verifica que se lance InvalidPhoneNumberError si el teléfono contiene caracteres no válidos."""
    gestor = GestorDeContactos()
    with pytest.raises(InvalidPhoneNumberError):
        gestor.agregar_contacto(Contacto("Luis", "abcdef1234", "luis@correo.com", "Amigo"))

def test_agregar_contacto_nombre_excesivamente_largo():
    """Verifica que se lance ContactError si el nombre del contacto excede los 200 caracteres."""
    gestor = GestorDeContactos()
    nombre_largo = "A" * 201 
    with pytest.raises(ContactError) as excinfo:
        gestor.agregar_contacto(Contacto(nombre_largo, "9876543210", "contacto@correo.com", "Amigo"))
    assert str(excinfo.value) == "El nombre no puede exceder los 200 caracteres."

def test_agregar_contacto_categoria_muy_larga():
    """Verifica que se lance ContactError si la categoría del contacto supera los 100 caracteres."""
    gestor = GestorDeContactos()
    with pytest.raises(ContactError):
        gestor.agregar_contacto(Contacto("Marta", "9876543210", "marta@correo.com", "A" * 101))
