import os

class ContactError(Exception):
    """
    Excepción base para errores relacionados con contactos.
    
    Args:
        mensaje (str): Mensaje descriptivo del error.
    """
    def __init__(self, mensaje):
        super().__init__(mensaje)

class InvalidPhoneNumberError(ContactError):
    """
    Excepción lanzada cuando el número de teléfono no es válido.

    Args:
        telefono (str): Número de teléfono que causó el error.
    """
    def __init__(self, telefono):
        super().__init__(f"Número de teléfono inválido: '{telefono}'. Debe contener al menos 10 dígitos y ser completamente numérico.")

class InvalidEmailError(ContactError):
    """
    Excepción lanzada cuando el correo electrónico tiene un formato inválido.

    Args:
        email (str): Email que causó el error.
    """
    def __init__(self, email):
        super().__init__(f"Correo electrónico inválido: '{email}'. Verifica que tenga un formato correcto (ejemplo@dominio.com).")

class InvalidEmailTooLong(Exception):
    """
    Excepción lanzada cuando un email excede la longitud máxima permitida.

    Args:
        email (str): Email que excedió la longitud.
        maximo_caracteres (int): Longitud máxima permitida.
    """
    def __init__(self, email, maximo_caracteres=255):
        super().__init__(f"Correo electrónico inválido: '{email}' supera el límite de {maximo_caracteres} caracteres.")

class ContactNotFoundError(Exception):
    """
    Excepción lanzada cuando no se encuentra un contacto por nombre.

    Args:
        nombre (str): Nombre del contacto no encontrado.
    """
    def __init__(self, nombre):
        super().__init__(f"El contacto con el nombre '{nombre}' no se encontró.")

class DuplicateContactError(Exception):
    """
    Excepción lanzada cuando se intenta agregar un contacto que ya existe.

    Args:
        nombre (str): Nombre del contacto duplicado.
    """
    def __init__(self, nombre):
        super().__init__(f"El contacto con el nombre '{nombre}' ya existe.")

class VCFExportError(Exception):
    """
    Excepción lanzada cuando ocurre un error durante la exportación de contactos a VCF.

    Args:
        mensaje (str): Mensaje de error descriptivo.
    """
    def __init__(self, mensaje):
        super().__init__(mensaje)

class VCFImportError(Exception):
    """
    Excepción lanzada cuando ocurre un error durante la importación de un archivo VCF.

    Args:
        mensaje (str): Mensaje de error descriptivo.
    """
    def __init__(self, mensaje):
        super().__init__(mensaje)

def exportar_a_vcf(self, archivo):
    """
    Lanza una excepción si no hay contactos para exportar a un archivo VCF.

    Args:
        archivo (str): Ruta del archivo a exportar.

    Raises:
        VCFExportError: Si no existen contactos para exportar.
    """
    if not self.contactos:
        raise VCFExportError("No hay contactos para exportar.")

def importar_desde_vcf(self, archivo):
    """
    Lanza una excepción si el archivo VCF especificado no existe.

    Args:
        archivo (str): Ruta del archivo VCF a importar.

    Raises:
        VCFImportError: Si el archivo no existe.
    """
    if not os.path.exists(archivo):
        raise VCFImportError("El archivo no existe.")

class InvalidNameError(ValueError):
    """
    Excepción lanzada cuando un nombre no es válido.
    """
    pass

class InvalidEmailError(ValueError):
    """
    Excepción lanzada cuando un email no es válido.
    """
    pass

class InvalidPasswordError(ValueError):
    """
    Excepción lanzada cuando una contraseña no es válida.
    """
    pass


