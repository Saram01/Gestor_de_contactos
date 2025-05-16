import bcrypt
from src.model.usuario import Usuario
from src.model.db import SessionLocal

session = SessionLocal()


class GestorDeUsuarios:
    """
    Clase que gestiona el registro y autenticación de usuarios utilizando SQLAlchemy.
    """

    def registrar_usuario(self, nombre: str, email: str, contrasena: str) -> str:
        session = SessionLocal()
        try:
            usuario_existente = session.query(Usuario).filter_by(email=email).first()
            if usuario_existente:
                return "El usuario ya está registrado."

            nuevo_usuario = Usuario(nombre=nombre, email=email, password=contrasena)
            session.add(nuevo_usuario)
            session.commit()
            return "Usuario registrado exitosamente."
        except Exception as e:
            session.rollback()
            return f"Error al registrar el usuario: {str(e)}"
        finally:
            session.close()

    def validar_credenciales(self, nombre_usuario: str, contrasena: str):
        session = SessionLocal()
        try:
            usuario = session.query(Usuario).filter_by(nombre_usuario=nombre_usuario).first()
            if usuario and usuario.verificar_contraseña(contrasena):
                return usuario
            return None
        finally:
            session.close()

    


