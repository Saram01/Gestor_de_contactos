import os
from src.model.db import SessionLocal, Contacto
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
        self.db = SessionLocal()

    def agregar_contacto(self, nombre, categoria, email, telefono, usuario_id):
        session = SessionLocal()
        """
        Agrega un contacto a la lista si su email no está duplicado.

        Args:
            contacto (Contacto): Objeto contacto a agregar.

        Raises:
            DuplicateContactError: Si ya existe un contacto con el mismo email.
        """
        try:
            nuevo_contacto = Contacto(
                nombre=nombre,
                categoria=categoria,
                email=email,
                telefono=telefono,
                usuario_id=usuario_id
            )
            self.db.add(nuevo_contacto)
            self.db.commit()
            return "Contacto agregado exitosamente."
        except Exception as e:
            self.db.rollback()
            return f"Error: {e}"

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
        contacto = self.db.query(Contacto).filter_by(email=email).first()
        if not contacto:
            raise ValueError(f"No se encontró ningún contacto con el correo {email}.")
        self.db.delete(contacto)
        self.db.commit()


    def buscar_contacto(self, nombre: str):
        """
        Busca contactos que contengan el nombre proporcionado.

        Args:
            nombre (str): Nombre o parte del nombre a buscar.

        Returns:
            list: Lista de contactos que coincidan con la búsqueda.
        """
        return self.db.query(Contacto).filter(Contacto.nombre.ilike(f"%{nombre}%")).all()
    
    def listar_contactos(self):
        """
        Lista todos los contactos almacenados.

        Returns:
            list: Lista completa de contactos.
        """
        return self.db.query(Contacto).all()

    def ordenar_contactos(self, clave="nombre"):
        """
        Ordena los contactos alfabéticamente según la clave proporcionada.

        Args:
            clave (str): Atributo del contacto por el cual ordenar.

        Returns:
            list: Lista de contactos ordenada.
        """
        return self.db.query(Contacto).order_by(getattr(Contacto, clave)).all()
    
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
        contacto = self.db.query(Contacto).filter_by(nombre=nombre).first()
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

        self.db.commit()
        

    def filtrar_contacto(self, categoria: str):
        """
        Filtra los contactos por una categoría específica.

        Args:
            categoria (str): Categoría a filtrar.

        Returns:
            list: Lista de contactos que pertenecen a esa categoría.
        """
        return self.db.query(Contacto).filter(Contacto.categoria.ilike(categoria)).all()
    
    def exportar_a_vcf(self, archivo: str):
        """
        Exporta los contactos actuales a un archivo VCF.

        Args:
            archivo (str): Ruta del archivo de salida.

        Raises:
            VCFExportError: Si ocurre un error durante la exportación.
        """
        try:
            contactos = self.listar_contactos()
            with open(archivo, 'w', encoding='utf-8') as f:
                for contacto in contactos:
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
                        nuevo = Contacto(**contacto_data)
                        if not self.db.query(Contacto).filter_by(email=nuevo.email).first():
                            self.db.add(nuevo)
                self.db.commit()
                print("Contactos importados exitosamente.")
        except Exception as e:
            print(f"Error al importar contactos: {e}")
            raise VCFImportError(str(e))
