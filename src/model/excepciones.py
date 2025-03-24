class ContactError(Exception):
    """Clase base para errores relacionados con contactos."""
    pass

class InvalidPhoneNumberError(ContactError):
    def __init__(self, telefono):
        super().__init__(f"Número de teléfono inválido: '{telefono}'. Debe contener al menos 10 dígitos y ser completamente numérico.")

class InvalidEmailError(ContactError):
    def __init__(self, email):
        super().__init__(f"Correo electrónico inválido: '{email}'. Verifica que tenga un formato correcto (ejemplo@dominio.com).")



class InvalidEmailTooLong(Exception):
    def __init__(self, email, maximo_caracteres=50):
        super().__init__(f"Correo electronico invalido ¿: {email}. Es muy largo")
    
    def validar_email(email, maximo_caracteres=50):
        if len(email)  > maximo_caracteres:
            raise
        InvalidEmailTooLong(email, maximo_caracteres)
        return True

class ContactNotFoundError(Exception):
    def __init__(self, nombre):
        super().__init__(f"El contacto '{nombre}' no fue encontrado en la lista.")

    def buscar_contacto(contactos, nombre):
        if nombre not in contactos:
            raise ContactNotFoundError(nombre)
        return contactos[nombre]

class DuplicateContactError(ContactError):
    def __init__(self, nombre):
        super().__init__(f"El contacto '{nombre}' ya existe en la lista.")

class VCFExportError(ContactError):
    def __init__(self, mensaje="Error al exportar contactos a archivo VCF. Verifique los datos y permisos del archivo."):
        super().__init__(mensaje)

class VCFImportError(ContactError):
    def __init__(self, mensaje="Error al importar contactos desde archivo VCF. Verifique la estructura del archivo y los datos."):
        super().__init__(mensaje)

