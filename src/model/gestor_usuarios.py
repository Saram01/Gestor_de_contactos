import bcrypt
from src.model.usuario import Usuario


class GestorDeUsuarios:
    def __init__(self):
        self.usuarios = []

    def registrar_usuario(self, nombre, email, password):
        for u in self.usuarios:
            if u.email == email:
                return "El usuario ya existe."
        usuario = Usuario(nombre, email, password)
        self.usuarios.append(usuario)
        return "Usuario registrado exitosamente."

    def validar_credenciales(self, email, password):
        for u in self.usuarios:
            if u.email == email and u.verificar_contraseña(password):
                return u
        return None

    


