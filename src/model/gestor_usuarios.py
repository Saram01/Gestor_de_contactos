import bcrypt
from src.model.usuario import Usuario

class GestorDeUsuarios:
    """
    Clase responsable de manejar el registro de usuarios y la validación de credenciales
    para iniciar sesión. Administra una lista interna de objetos Usuario.
    """

    def __init__(self):
        """
        Inicializa una lista vacía de usuarios.
        """
        self.usuarios = []  # Lista de instancias de `Usuario`

    def registrar_usuario(self, nombre, email, contraseña):
        """
        Registra un nuevo usuario si el email no ha sido utilizado previamente.

        Args:
            nombre (str): Nombre del usuario.
            email (str): Correo electrónico del usuario.
            contraseña (str): Contraseña en texto plano (se encripta internamente).

        Returns:
            str: Mensaje indicando si el usuario fue registrado exitosamente o si el email ya existe.
        """
        if any(u.email == email for u in self.usuarios):
            return "El correo ya está registrado."
        
        # Crear nuevo usuario y agregarlo a la lista.
        nuevo_usuario = Usuario(nombre, email, contraseña)
        self.usuarios.append(nuevo_usuario)
        return "Usuario registrado exitosamente"

    def validar_credenciales(self, email, password):
        """
        Valida las credenciales de un usuario al iniciar sesión.

        Args:
            email (str): Correo electrónico del usuario.
            password (str): Contraseña en texto plano.

        Returns:
            Usuario or None: Devuelve la instancia de Usuario si las credenciales son válidas,
                             de lo contrario, devuelve None.
        """
        for usuario in self.usuarios:
            if usuario.email == email and bcrypt.checkpw(password.encode(), usuario.password):
                return usuario
        return None
