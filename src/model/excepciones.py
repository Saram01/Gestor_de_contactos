class ContactError(Exception):
    def __init__(self, mensaje):
        super().__init__(mensaje)

class InvalidPhoneNumberError(ContactError):
    def __init__(self, telefono):
        super().__init__(f"Número de teléfono inválido: '{telefono}'. Debe contener al menos 10 dígitos y ser completamente numérico.")

class InvalidEmailError(ContactError):
    def __init__(self, email):
        super().__init__(f"Correo electrónico inválido: '{email}'. Verifica que tenga un formato correcto (ejemplo@dominio.com).")

class InvalidEmailTooLong(Exception):
    def __init__(self, email, maximo_caracteres=255):
        super().__init__(f"Correo electrónico inválido: '{email}' supera el límite de {maximo_caracteres} caracteres.")

class ContactNotFoundError(Exception):
    def __init__(self, nombre):
        super().__init__(f"El contacto con el nombre '{nombre}' no se encontró.")

class DuplicateContactError(Exception):
    def __init__(self, nombre):
        super().__init__(f"El contacto con el nombre '{nombre}' ya existe.")

class VCFExportError(Exception):
    def __init__(self, mensaje):
        super().__init__(mensaje)

class VCFImportError(Exception):
    def __init__(self, mensaje):
        super().__init__(mensaje)

def exportar_a_vcf(self, archivo):
    if not self.contactos:
        raise VCFExportError("No hay contactos para exportar.")

def importar_desde_vcf(self, archivo):
    if not os.path.exists(archivo):
        raise VCFImportError("El archivo no existe.")

class InvalidNameError(ValueError):
    pass

class InvalidEmailError(ValueError):
    pass

class InvalidPasswordError(ValueError):
    pass



