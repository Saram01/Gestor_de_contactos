import psycopg2
import bcrypt
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
                return usuario
        return None
    
    def crear_usuario(nombre: str, email: str, password: str):
        usuario = Usuario(nombre, email, password)
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO usuario (nombre_usuario, contrasena) VALUES (%s, %s)",
                (usuario.nombre, usuario.password)
            )
            conn.commit()
            print(f"✅ Usuario '{usuario.nombre}' creado correctamente.")
        except psycopg2.Error as e:
            conn.rollback()
            print(f"❌ Error al crear usuario: {e}")
        finally:
            cursor.close()
            conn.close()

    


