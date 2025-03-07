class ContactError(Exception):
    pass

class InvalidPhoneNumberError(ContactError):
    def __init__(self, telefono):
        super().__init__(f"Número de teléfono inválido: {telefono}. Debe contener al menos 10 dígitos y ser numérico.")

class InvalidEmailError(ContactError):
    def __init__(self, email):
        super().__init__(f"Correo electrónico inválido: {email}. Debe contener '@' y '.'.")



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
        super().__init__(f"El contacto '{nombre}' no fue encontrado.")

    def buscar_contacto(contactos, nombre):
        if nombre not in contactos:
            raise ContactNotFoundError(nombre)
        return contactos[nombre]

class DuplicateContactError(ContactError):
    def __init__(self, nombre):
        super().__init__(f"El contacto '{nombre}' ya existe.")

class VCFExportError(Exception):
    def __init__(self, mensaje="Error al exportar contactos a archivo VCF."):
        super().__init__(mensaje)

class VCFImportError(Exception):
    def __init__(self, mensaje="Error al importar contactos desde archivo VCF."):
        super().__init__(mensaje)
