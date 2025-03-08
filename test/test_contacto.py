import pytest
from src.model.excepciones import (InvalidPhoneNumberError, InvalidEmailError, 
                             ContactNotFoundError, DuplicateContactError, 
                             VCFExportError, VCFImportError, ContactError)
from src.model.contactos import Contacto
from src.model.gestor_contactos import GestorDeContactos
from src.model.usuario import Usuario

def validar_contacto(nombre, telefono, email):
    if not nombre:
        raise ContactError("El nombre del contacto no puede estar vacío.")
    
    if not telefono.isdigit() or len(telefono) < 10:
        raise InvalidPhoneNumberError(telefono)
    
    if "@" not in email or "." not in email:
        raise InvalidEmailError(email)

def test_contacto_no_encontrado(ContactNotFoundError):
    contactos = {"Alice", 
                 "Bob", 
                 "Jaime"}
    with pytest.raises(ContactNotFoundError) as exc_info:
        buscar_contacto(contactos, "Vanessa")
        assert  "El contacto no se encontro" in str(exc_info.value)


def test_email_invalido_muy_largo():
    with pytest.raises(InvalidEmailTooLong):
        validar_contacto("Laura", "9876543215", "lauraaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa@correo.com")
  
    
def test_crear_contacto_valido():
    contacto = Contacto("Luis", "123456789", "luis@example.com", "Amigo")
    assert contacto.nombre == "Luis"
    assert contacto.telefono == "123456789"
    assert contacto.email == "luis@correo.com"
    assert contacto.categoria == "Amigo"

def test_telefono_invalido_muy_corto():
    with pytest.raises(InvalidPhoneNumberError):
        validar_contacto("Luis", "123", "luis@correo.com")

def test_telefono_invalido_no_numerico():
    with pytest.raises(InvalidPhoneNumberError):
        validar_contacto("Ana", "ABC1234", "ana@correo.com")

def test_telefono_demasiado_largo():
    with pytest.raises(InvalidPhoneNumberError):
        validar_contacto("Pedro", "1234567890123456", "pedro@correo.com")

def test_email_invalido_sin_arroba():
    with pytest.raises(InvalidEmailError):
        validar_contacto("Carlos", "987654321", "carlos.correo.com")

def test_email_invalido_sin_punto():
    with pytest.raises(InvalidEmailError):
        validar_contacto("Maria", "987654321", "maria@correocom")

def test_email_valido_con_caracteres_especiales():
    contacto = Contacto("Ana", "987654321", "ana+test@correo.com", "Familia")
    assert contacto.email == "ana+test@correo.com"

def test_nombre_vacio():
    with pytest.raises(ContactError):
        validar_contacto("", "987654321", "test@correo.com")

def test_telefono_vacio():
    with pytest.raises(InvalidPhoneNumberError):
        validar_contacto("Carlos", "", "carlos@correo.com")

def test_email_vacio():
    with pytest.raises(InvalidEmailError):
        validar_contacto("Carlos", "987654321", "")

def test_categoria_vacia():
    contacto = Contacto("Luis", "123456789", "luis@correo.com", "")
    assert contacto.categoria == ""

def test_nombre_con_caracteres_especiales():
    contacto = Contacto("Lu!s@", "123456789", "luis@correo.com", "Amigo")
    assert contacto.nombre == "Lu!s@"
    
# parte de Jenn

def test_email_sin_dominio_valido():
    with pytest.raises(InvalidEmailError):
        validar_contacto("Sofia", "9876543210", "sofia@correo", "Amigo")
#2
def test_contacto_duplicado():
    gestor = GestorDeContactos()
    gestor.agregar_contacto("Daniel", "1234567890", "daniel@correo.com", "Trabajo")
    with pytest.raises(DuplicateContactError):
        gestor.agregar_contacto("Daniel", "1234567890", "daniel@correo.com", "Trabajo")
#3
def test_modificar_contacto_inexistente():
    gestor = GestorDeContactos()
    with pytest.raises(ContactNotFoundError):
        gestor.modificar_contacto("0000000000", "Nuevo Nombre", "nuevo@correo.com", "Amigo")
#4
def test_exportar_contactos_error():
    gestor = GestorDeContactos()
    with pytest.raises(VCFExportError):
        gestor.exportar_a_vcf("/ruta/invalida/contactos.vcf")
#5
def test_importar_contactos_vcf_corrupto():
    gestor = GestorDeContactos()
    with pytest.raises(VCFImportError):
        gestor.importar_desde_vcf("/ruta/invalida/contactos_corruptos.vcf")
#7
def test_nombre_solo_espacios():
    with pytest.raises(ContactError):
        validar_contacto("   ", "9876543210", "espacios@correo.com")
#8
def test_buscar_contacto_telefono_invalido():
    gestor = GestorDeContactos()
    with pytest.raises(InvalidPhoneNumberError):
        gestor.buscar_contacto("+12-34567890")
#9
def test_agregar_contacto_nombre_excesivamente_largo():
    gestor = GestorDeContactos()
    nombre_largo = "A" * 300  # Un nombre de 300 caracteres
    with pytest.raises(ContactError):
        gestor.agregar_contacto(nombre_largo, "9876543210", "contacto@correo.com", "Amigo")
