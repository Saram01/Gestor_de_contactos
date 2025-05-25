from src.model.contactos import Contacto
from src.model.usuario import Usuario

class StorageMemoria:
    def __init__(self):
        self.usuarios = []

    def agregar_usuario(self, usuario):
        if any(u.email == usuario.email for u in self.usuarios):
            raise ValueError(f"El usuario con el correo {usuario.email} ya existe.")
        self.usuarios.append(usuario)

    def listar_usuarios(self):
        return self.usuarios

    def agregar_contacto(self, usuario, contacto):
        if any(c.email == contacto.email for c in usuario.contactos):
            raise ValueError(f"El contacto con el correo {contacto.email} ya existe.")
        usuario.contactos.append(contacto)

    def listar_contactos(self, usuario):
        return usuario.contactos

    def eliminar_contacto(self, usuario, email):
        for c in usuario.contactos:
            if c.email == email:
                usuario.contactos.remove(c)
                return
        raise ValueError(f"No se encontró ningún contacto con el correo {email}.")

class StorageDB:
    def __init__(self, session):
        self.session = session

    def agregar_usuario(self, usuario):
        if self.session.query(Usuario).filter_by(email=usuario.email).first():
            raise ValueError(f"El usuario con el correo {usuario.email} ya existe.")
        self.session.add(usuario)
        self.session.commit()

    def listar_usuarios(self):
        return self.session.query(Usuario).all()

    def agregar_contacto(self, usuario, contacto):
        contacto.usuario_id = usuario.id
        if self.session.query(Contacto).filter_by(email=contacto.email, usuario_id=usuario.id).first():
            raise ValueError(f"El contacto con el correo {contacto.email} ya existe.")
        self.session.add(contacto)
        self.session.commit()

    def listar_contactos(self, usuario):
        return self.session.query(Contacto).filter_by(usuario_id=usuario.id).all()

    def eliminar_contacto(self, usuario, email):
        contacto = self.session.query(Contacto).filter_by(email=email, usuario_id=usuario.id).first()
        if contacto:
            self.session.delete(contacto)
            self.session.commit()
        else:
            raise ValueError(f"No se encontró ningún contacto con el correo {email}.")