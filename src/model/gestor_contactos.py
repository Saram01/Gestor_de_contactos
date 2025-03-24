import os
from src.model.contactos import Contacto
from src.model.excepciones import (DuplicateContactError, InvalidPhoneNumberError, InvalidEmailError, ContactNotFoundError, ContactError, VCFExportError, VCFImportError)

class GestorDeContactos:
    def __init__(self):
        self.contactos = []

    def agregar_contacto(self, contacto: Contacto):
        if any(c.email == contacto.email for c in self.contactos):
            raise DuplicateContactError(contacto.nombre)
        self.contactos.append(contacto)

    def eliminar_contacto(self, email: str):
        if not email.strip():
            raise ContactError("El correo proporcionado no puede estar vacío.")

        if not any(c.email == email for c in self.contactos):
            raise ValueError(f"No se encontró ningún contacto con el correo {email}.")
        self.contactos = [c for c in self.contactos if c.email != email]


    def buscar_contacto(self, nombre: str):
        return [c for c in self.contactos if nombre.lower() in c.nombre.lower()]

    def listar_contactos(self):
        return self.contactos

    def ordenar_contactos(self, clave="nombre"):
        return sorted(self.contactos, key=lambda c: getattr(c, clave, "").lower())
    
    def editar_contacto(self, nombre: str, telefono: str = None, email: str = None, categoria: str = None):
        if not nombre.strip():
            raise ContactNotFoundError(nombre)
        for contacto in self.contactos:
            if contacto.nombre.lower() == nombre.lower():
                if telefono:
                    if not Contacto.validar_numero(telefono):
                        raise InvalidPhoneNumberError(telefono)
                    contacto.telefono = telefono
                if email:
                    if not Contacto.validar_email(email):
                        raise InvalidEmailError(email)
                    contacto.email = email
                if categoria is not None:
                    contacto.categoria = categoria
                return
        raise ContactNotFoundError(nombre)

    def filtrar_contacto(self, categoria: str):
        return [c for c in self.contactos if c.categoria.lower() == categoria.lower()]
    
    def exportar_a_vcf(self, archivo):
        if not self.contactos:
            raise VCFExportError("No hay contactos para exportar.")
        try:
            with open(archivo, "w") as f:
                for contacto in self.contactos:
                    f.write(f"BEGIN:VCARD\nVERSION:3.0\n")
                    f.write(f"N:{contacto.nombre}\n")
                    f.write(f"TEL:{contacto.telefono}\n")
                    f.write(f"EMAIL:{contacto.email}\n")
                    f.write(f"CATEGORY:{contacto.categoria}\n")
                    f.write("END:VCARD\n")
        except FileNotFoundError:
            raise VCFExportError(f"No se pudo escribir en el archivo {archivo}.")

    def importar_desde_vcf(self, archivo):
        if not os.path.exists(archivo):
            raise VCFImportError(f"El archivo {archivo} no existe.")




