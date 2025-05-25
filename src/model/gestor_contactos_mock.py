from src.model.contactos import Contacto
from src.model.excepciones import (
    DuplicateContactError, InvalidPhoneNumberError, InvalidEmailError,
    ContactNotFoundError, ContactError, VCFExportError, VCFImportError
)
import os

class GestorDeContactosMock:
    def __init__(self):
        self.contactos = []

    def agregar_contacto(self, nombre, categoria, email, telefono, usuario_id=None):
        if any(c.email == email for c in self.contactos):
            raise DuplicateContactError(f"Ya existe un contacto con email {email}")
        nuevo = Contacto(nombre, categoria, email, telefono, usuario_id)
        self.contactos.append(nuevo)
        return "Contacto agregado exitosamente."

    def eliminar_contacto(self, email):
        if not email.strip():
            raise ContactError("El correo proporcionado no puede estar vacío.")
        for c in self.contactos:
            if c.email == email:
                self.contactos.remove(c)
                return
        raise ValueError(f"No se encontró ningún contacto con el correo {email}.")

    def buscar_contacto(self, nombre):
        return [c for c in self.contactos if nombre.lower() in c.nombre.lower()]

    def listar_contactos(self):
        return self.contactos

    def ordenar_contactos(self, clave="nombre"):
        return sorted(self.contactos, key=lambda c: getattr(c, clave))

    def editar_contacto(self, nombre, telefono=None, email=None, categoria=None):
        contacto = next((c for c in self.contactos if c.nombre == nombre), None)
        if not contacto:
            raise ContactNotFoundError(nombre)
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

    def filtrar_contacto(self, categoria):
        return [c for c in self.contactos if c.categoria.lower() == categoria.lower()]

    def exportar_a_vcf(self, archivo):
        try:
            with open(archivo, 'w', encoding='utf-8') as f:
                for contacto in self.contactos:
                    f.write(f"BEGIN:VCARD\n")
                    f.write(f"VERSION:3.0\n")
                    f.write(f"N:{contacto.nombre}\n")
                    f.write(f"TEL:{contacto.telefono}\n")
                    f.write(f"EMAIL:{contacto.email}\n")
                    if contacto.categoria:
                        f.write(f"CATEGORY:{contacto.categoria}\n")
                    f.write(f"END:VCARD\n")
            print(f"Contactos exportados exitosamente a {archivo}")
        except Exception as e:
            print(f"Error al exportar contactos: {e}")
            raise VCFExportError(str(e))

    def importar_desde_vcf(self, archivo):
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                contacto_data = {}
                for linea in f:
                    linea = linea.strip()
                    if linea.startswith("BEGIN:VCARD"):
                        contacto_data = {}
                    elif linea.startswith("N:"):
                        contacto_data["nombre"] = linea.split(":", 1)[1]
                    elif linea.startswith("TEL:"):
                        contacto_data["telefono"] = linea.split(":", 1)[1]
                    elif linea.startswith("EMAIL:"):
                        contacto_data["email"] = linea.split(":", 1)[1]
                    elif linea.startswith("CATEGORY:"):
                        contacto_data["categoria"] = linea.split(":", 1)[1]
                    elif linea.startswith("END:VCARD"):
                        contacto_data["usuario_id"] = 1
                        if not any(c.email == contacto_data["email"] for c in self.contactos):
                            nuevo = Contacto(**contacto_data)
                            self.contactos.append(nuevo)
                print("Contactos importados exitosamente.")
        except Exception as e:
            print(f"Error al importar contactos: {e}")
            raise VCFImportError(str(e))
