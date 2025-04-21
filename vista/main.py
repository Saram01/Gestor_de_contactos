import bcrypt
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.screenmanager import Screen
from src.model.gestor_usuarios import GestorDeUsuarios
from src.model.contactos import Contacto
from src.model.excepciones import (
                                    InvalidNameError,
                                    InvalidEmailError,
                                    InvalidPasswordError,)

gestor_usuarios = GestorDeUsuarios()

class LoginScreen(Screen):
    def iniciar_sesion(self):
        try:
            email = self.ids.email_input.text.strip()
            password = self.ids.password_input.text.strip()
            print(f"Email: {email}, Password: {password}")

            if not email or not password:
                self.ids.message_label.text = "Por favor, completa todos los campos."
                return

            usuario = gestor_usuarios.validar_credenciales(email, password)
            if usuario:
                print(f"Usuario encontrado: {usuario.nombre}")
                self.manager.current = 'menu'
                print("Cambiando a pantalla 'menu'")
                self.manager.get_screen('menu').ids.welcome_label.text = f"Bienvenido, {usuario.nombre}!"
            else:
                self.ids.message_label.text = "Error: Credenciales inválidas."
        except AttributeError as e:
            print(f"Atributo no encontrado: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")




class RegisterScreen(Screen):
    def registrar_usuario(self):
        try:
            nombre = self.ids.nombre_input.text.strip()
            email = self.ids.email_input.text.strip()
            password = self.ids.password_input.text.strip()

            if not nombre:
                self.ids.message_label.text = "El nombre no puede estar vacío."
                return
            if not email:
                self.ids.message_label.text = "El correo no puede estar vacío."
                return
            if not password:
                self.ids.message_label.text = "La contraseña no puede estar vacía."
                return

            # Intentar registrar al usuario.
            mensaje = gestor_usuarios.registrar_usuario(nombre, email, password)
            if "Usuario registrado exitosamente" in mensaje:
                self.ids.message_label.text = "¡Usuario registrado exitosamente! Por favor, inicia sesión."
                self.manager.current = 'login'
            else:
                self.ids.message_label.text = mensaje
        except InvalidEmailError as e:
            self.ids.message_label.text = str(e)  # Mostrar el error al usuario
        except Exception as e:
            self.ids.message_label.text = "Ha ocurrido un error inesperado. Por favor, inténtalo de nuevo."
            print(f"Error inesperado: {e}")  # Imprime el error en la consola para depuración



class MenuScreen(Screen):
    def buscar_contacto(self):
        # Obtener el nombre del campo de entrada
        nombre = self.ids.buscar_nombre_input.text.strip()
        
        if not nombre:
            self.ids.contactos_label.text = "Por favor, introduce un nombre para buscar."
            return

        # Buscar en la lista de contactos del último usuario registrado
        try:
            usuario_actual = gestor_usuarios.usuarios[-1]
            resultados = [contacto for contacto in usuario_actual.obtener_contactos if contacto.nombre.lower() == nombre.lower()]
            
            if resultados:
                self.ids.contactos_label.text = f"Contactos encontrados: {', '.join([c.nombre for c in resultados])}"
            else:
                self.ids.contactos_label.text = "No se encontraron contactos con ese nombre."
        except IndexError:
            self.ids.contactos_label.text = "No hay usuarios registrados aún."

    def agregar_contacto(self):
        # Recuperar los datos del formulario
        nombre = self.ids.nombre_input.text.strip()
        telefono = self.ids.telefono_input.text.strip()
        email = self.ids.email_input.text.strip()
        categoria = self.ids.categoria_input.text.strip()

        if not nombre or not telefono or not email:
            self.ids.contactos_label.text = "Por favor, completa los campos obligatorios: Nombre, Teléfono y Email."
            return

        try:
            nuevo_contacto = Contacto(nombre=nombre, telefono=telefono, email=email, categoria=categoria)
            usuario_actual = gestor_usuarios.usuarios[-1]
            usuario_actual.agregar_contacto(nuevo_contacto)
            self.ids.contactos_label.text = f"Contacto agregado exitosamente: {nombre}"
        except IndexError:
            self.ids.contactos_label.text = "No hay usuarios registrados para agregar contactos."
        except ValueError as e:
            self.ids.contactos_label.text = str(e)

    def listar_contactos(self):
        # Listar todos los contactos del usuario actual
        try:
            usuario_actual = gestor_usuarios.usuarios[-1]
            contactos = usuario_actual.obtener_contactos
            if contactos:
                self.ids.contactos_label.text = '\n'.join([f"{c.nombre} - {c.email}" for c in contactos])
            else:
                self.ids.contactos_label.text = "No hay contactos registrados."
        except IndexError:
            self.ids.contactos_label.text = "No hay usuarios registrados."

    def eliminar_contacto(self):
        email = self.ids.eliminar_email_input.text.strip()
        if not email:
            self.ids.contactos_label.text = "Por favor, introduce un email para eliminar."
            return

        try:
            usuario_actual = gestor_usuarios.usuarios[-1]
            usuario_actual.contactos = [c for c in usuario_actual.obtener_contactos if c.email != email]
            self.ids.contactos_label.text = f"El contacto con el correo {email} ha sido eliminado."
        except IndexError:
            self.ids.contactos_label.text = "No hay usuarios registrados."
        except Exception as e:
            self.ids.contactos_label.text = str(e)

    def editar_contacto(self):
        try:
            nombre_actual = self.ids.editar_nombre_actual_input.text.strip()
            nombre_nuevo = self.ids.editar_nombre_nuevo_input.text.strip()
            telefono_nuevo = self.ids.editar_telefono_nuevo_input.text.strip()
            email_nuevo = self.ids.editar_email_nuevo_input.text.strip()
            categoria_nueva = self.ids.editar_categoria_nueva_input.text.strip()

            usuario_actual = gestor_usuarios.usuarios[-1]
            contacto = next((c for c in usuario_actual.obtener_contactos if c.nombre.lower() == nombre_actual.lower()), None)

            if not contacto:
                self.ids.editar_message_label.text = f"No se encontró ningún contacto con el nombre '{nombre_actual}'."
                return

            if nombre_nuevo:
                contacto.nombre = nombre_nuevo
            if telefono_nuevo:
                contacto.telefono = telefono_nuevo
            if email_nuevo:
                contacto.email = email_nuevo
            if categoria_nueva:
                contacto.categoria = categoria_nueva

            self.ids.editar_message_label.text = f"Contacto '{nombre_actual}' actualizado exitosamente."
        except IndexError:
            self.ids.editar_message_label.text = "No hay usuarios registrados."
        except Exception as e:
            self.ids.editar_message_label.text = str(e)

    def exportar_contactos(self):
        archivo = self.ids.exportar_archivo_input.text.strip()
        if not archivo:
            self.ids.contactos_label.text = "Por favor, introduce un nombre de archivo para exportar."
            return

        try:
            usuario_actual = gestor_usuarios.usuarios[-1]  # Último usuario registrado
            usuario_actual.exportar_a_vcf(archivo)
            self.ids.contactos_label.text = f"Contactos exportados exitosamente a '{archivo}'."
        except IndexError:
            self.ids.contactos_label.text = "No hay usuarios registrados."
        except Exception as e:
            self.ids.contactos_label.text = f"Error al exportar contactos: {str(e)}"


    def importar_contactos(self):
        archivo = self.ids.importar_archivo_input.text.strip()
        if not archivo:
            self.ids.contactos_label.text = "Por favor, introduce un nombre de archivo para importar."
            return

        try:
            usuario_actual = gestor_usuarios.usuarios[-1]  # Último usuario registrado
            usuario_actual.importar_desde_vcf(archivo)
            self.ids.contactos_label.text = "Contactos importados exitosamente."
            self.listar_contactos()  # Refrescar la lista en la interfaz
        except IndexError:
            self.ids.contactos_label.text = "No hay usuarios registrados."
        except Exception as e:
            self.ids.contactos_label.text = f"Error al importar contactos: {str(e)}"




class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(MenuScreen(name='menu'))
        return sm

    

if __name__ == '__main__':
    try:
        MainApp().run()
    except Exception as e:
        print(f"Se ha producido un error inesperado: {e}")

