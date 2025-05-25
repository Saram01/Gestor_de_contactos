import sys
import os

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from src.model.gestor_usuarios import GestorDeUsuarios
from src.model.gestor_contactos import GestorDeContactos
from src.model.contactos import Contacto
from src.model.usuario import Usuario
from src.model.storage import StorageMemoria, StorageDB

try:
    from src.model.db import SessionLocal, crear_tablas
    crear_tablas()
    session = SessionLocal()
    storage = StorageDB(session)
    print("Conectado a la base de datos.")
except Exception as e:
    storage = StorageMemoria()
    print("No se pudo conectar a la base de datos. Usando almacenamiento en memoria.")
gestor_usuarios = GestorDeUsuarios(storage)

class LoginScreen(Screen):
    def iniciar_sesion(self):
        email = self.ids.email_input.text.strip()
        password = self.ids.password_input.text.strip()

        if not email or not password:
            self.ids.message_label.text = "Por favor completa todos los campos."
            return

        usuario = gestor_usuarios.validar_credenciales(email, password)
        if usuario:
            self.manager.get_screen('menu').usuario_actual = usuario
            self.manager.get_screen('menu').gestor_contactos = GestorDeContactos(usuario, storage)
            self.manager.current = 'menu'
            self.manager.get_screen('menu').ids.welcome_label.text = f"Bienvenido, {usuario.nombre_usuario}!"
            self.ids.message_label.text = ""
        else:
            self.ids.message_label.text = "Credenciales inválidas."

class RegisterScreen(Screen):
    def registrar_usuario(self):
        nombre = self.ids.nombre_input.text.strip()
        email = self.ids.email_input.text.strip()
        password = self.ids.password_input.text.strip()

        if not nombre or not email or not password:
            self.ids.message_label.text = "Completa todos los campos."
            return

        mensaje = gestor_usuarios.registrar_usuario(nombre, email, password)
        self.ids.message_label.text = mensaje
        if "exitosamente" in mensaje:
            self.manager.current = 'login'

class MenuScreen(Screen):
    usuario_actual = None
    gestor_contactos = None

    def agregar_contacto(self):
        nombre = self.ids.nombre_input.text.strip()
        telefono = self.ids.telefono_input.text.strip()
        email = self.ids.email_input.text.strip()
        categoria = self.ids.categoria_input.text.strip()

        if not nombre or not telefono or not email:
            self.ids.info_label.text = "Completa Nombre, Teléfono y Email."
            return

        nuevo_contacto = Contacto(nombre, telefono, email, categoria)
        self.gestor_contactos.agregar_contacto(nuevo_contacto)
        self.ids.info_label.text = f"Contacto '{nombre}' agregado."

    def listar_contactos(self):
        contactos = self.gestor_contactos.listar_contactos()
        if contactos:
            texto = '\n'.join([f"{c.nombre} - {c.email}" for c in contactos])
            self.ids.info_label.text = texto
        else:
            self.ids.info_label.text = "No hay contactos."

    def cerrar_sesion(self):
        self.usuario_actual = None
        self.manager.current = 'login'

class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(MenuScreen(name='menu'))
        return sm

if __name__ == '__main__':
    MainApp().run()

