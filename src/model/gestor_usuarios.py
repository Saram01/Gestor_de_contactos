from src.model.usuario import Usuario

class GestorDeUsuarios:
    def __init__(self):
        self.usuarios = []

    def registrar_usuario(self, nombre: str, email: str, contraseña: str):
        if any(user.email == email for user in self.usuarios):
            return "Error: Ya existe un usuario con este email."
        nuevo_usuario = Usuario(nombre, email, contraseña)
        self.usuarios.append(nuevo_usuario)
        return "Usuario registrado exitosamente."

    def validar_credenciales(self, email: str, contraseña: str):
        for usuario in self.usuarios:
            if usuario.email == email and usuario.contraseña == contraseña:
                return usuario
        return "Error: Credenciales inválidas."
