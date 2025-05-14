import os
from src.model.contactos import Contacto
from src.model.excepciones import (
    DuplicateContactError, InvalidPhoneNumberError, InvalidEmailError,
    ContactNotFoundError, ContactError, VCFExportError, VCFImportError
)

class GestorDeContactos:
    """
    Clase para gestionar una lista de contactos, incluyendo operaciones de agregar,
    eliminar, editar, buscar, filtrar y exportar/importar contactos en formato VCF.
    """

    def __init__(self):
        """Inicializa una lista vacía de contactos."""
        self.contactos = []

    def agregar_contacto(self, contacto: Contacto):
        """
        Agrega un contacto a la lista si su email no está duplicado.

        Args:
            contacto (Contacto): Objeto contacto a agregar.

        Raises:
            DuplicateContactError: Si ya existe un contacto con el mismo email.
        """
        if any(c.email == contacto.email for c in self.contactos):
            raise DuplicateContactError(contacto.nombre)
        self.contactos.append(contacto)

    def eliminar_contacto(self, email: str):
        """
        Elimina un contacto según su email.

        Args:
            email (str): Email del contacto a eliminar.

        Raises:
            ContactError: Si el email está vacío.
            ValueError: Si no se encuentra un contacto con el email especificado.
        """
        if not email.strip():
            raise ContactError("El correo proporcionado no puede estar vacío.")

        if not any(c.email == email for c in self.contactos):
            raise ValueError(f"No se encontró ningún contacto con el correo {email}.")
        self.contactos = [c for c in self.contactos if c.email != email]

    def buscar_contacto(self, nombre: str):
        """
        Busca contactos que contengan el nombre proporcionado.

        Args:
            nombre (str): Nombre o parte del nombre a buscar.

        Returns:
            list: Lista de contactos que coincidan con la búsqueda.
        """
        return [c for c in self.contactos if nombre.lower() in c.nombre.lower()]

    def listar_contactos(self):
        """
        Lista todos los contactos almacenados.

        Returns:
            list: Lista completa de contactos.
        """
        return self.contactos

    def ordenar_contactos(self, clave="nombre"):
        """
        Ordena los contactos alfabéticamente según la clave proporcionada.

        Args:
            clave (str): Atributo del contacto por el cual ordenar.

        Returns:
            list: Lista de contactos ordenada.
        """
        return sorted(self.contactos, key=lambda c: getattr(c, clave, "").lower())
    
    def editar_contacto(self, nombre: str, telefono: str = None, email: str = None, categoria: str = None):
        """
        Edita los datos de un contacto existente.

        Args:
            nombre (str): Nombre del contacto a editar.
            telefono (str, optional): Nuevo teléfono.
            email (str, optional): Nuevo email.
            categoria (str, optional): Nueva categoría.

        Raises:
            ContactNotFoundError: Si no se encuentra el contacto por nombre.
            InvalidPhoneNumberError: Si el número de teléfono no es válido.
            InvalidEmailError: Si el email no es válido.
        """
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
        """
        Filtra los contactos por una categoría específica.

        Args:
            categoria (str): Categoría a filtrar.

        Returns:
            list: Lista de contactos que pertenecen a esa categoría.
        """
        return [c for c in self.contactos if c.categoria.lower() == categoria.lower()]
    
    def exportar_a_vcf(self, archivo: str):
        """
        Exporta los contactos actuales a un archivo VCF.

        Args:
            archivo (str): Ruta del archivo de salida.

        Raises:
            VCFExportError: Si ocurre un error durante la exportación.
        """
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

    def importar_desde_vcf(self, archivo: str):
        """
        Importa contactos desde un archivo VCF.

        Args:
            archivo (str): Ruta del archivo de entrada.

        Raises:
            VCFImportError: Si ocurre un error durante la importación.
        """
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                contacto = {}
                for linea in f:
                    linea = linea.strip()
                    if linea.startswith("BEGIN:VCARD"):
                        contacto = {}
                    elif linea.startswith("N:"):
                        contacto["nombre"] = linea.split(":")[1]
                    elif linea.startswith("TEL:"):
                        contacto["telefono"] = linea.split(":")[1]
                    elif linea.startswith("EMAIL:"):
                        contacto["email"] = linea.split(":")[1]
                    elif linea.startswith("CATEGORY:"):
                        contacto["categoria"] = linea.split(":")[1]
                    elif linea.startswith("END:VCARD"):
                        nuevo_contacto = Contacto(
                            nombre=contacto.get("nombre"),
                            telefono=contacto.get("telefono"),
                            email=contacto.get("email"),
                            categoria=contacto.get("categoria"),
                        )
                        self.contactos.append(nuevo_contacto)
            print("Contactos importados exitosamente.")
        except Exception as e:
            print(f"Error al importar contactos: {e}")
            raise VCFImportError(str(e))
