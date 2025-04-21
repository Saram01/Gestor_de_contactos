from src.model.usuario import Usuario

class GestorDeUsuarios:
    def __init__(self):
        self.usuarios = []  # Lista de instancias de `Usuario`

    def registrar_usuario(self, nombre, email, contraseña):
        if any(u.email == email for u in self.usuarios):
            return "El correo ya está registrado."
        
        # Crear nuevo usuario y agregarlo a la lista.
        nuevo_usuario = Usuario(nombre, email, contraseña)
        self.usuarios.append(nuevo_usuario)
        return "Usuario registrado exitosamente"

    def validar_credenciales(self, email, password):
        for usuario in self.usuarios:
            if usuario.email == email and bcrypt.checkpw(password.encode(), usuario.password):
                return usuario  # Devuelve la instancia de Usuario
        return None

