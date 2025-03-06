from src.model.contactos import Contacto

class GestorDeContactos:
    def __init__(self):
        self.contactos = []

    def agregar_contacto(self, contacto: Contacto):
        self.contactos.append(contacto)

    def eliminar_contacto(self, email: str):
        self.contactos = [c for c in self.contactos if c.email != email]

    def buscar_contacto(self, nombre: str):
        return [c for c in self.contactos if nombre.lower() in c.nombre.lower()]

    def listar_contactos(self):
        return self.contactos