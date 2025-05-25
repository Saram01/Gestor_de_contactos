import bcrypt
from src.model.usuario import Usuario

class GestorDeUsuarios:
    def __init__(self, storage):
        self.storage = storage

    def registrar_usuario(self, nombre, email, password):
        # Buscar si ya existe el usuario
        usuarios = self.storage.listar_usuarios()
        for u in usuarios:
            if u.email == email:
                return "El usuario ya existe."
        usuario = Usuario(nombre_usuario=nombre, email=email, password=password)
        self.storage.agregar_usuario(usuario)
        return "Usuario registrado exitosamente."

    def validar_credenciales(self, email, password):
        usuarios = self.storage.listar_usuarios()
        for u in usuarios:
            if u.email == email and u.verificar_contraseña(password):
                return u
        return None
    


