import sys
from src.model.gestor_contactos import GestorDeContactos
from src.model.contactos import Contacto
from src.model.usuario import Usuario
from src.model.gestor_usuarios import GestorDeUsuarios

def menu():
    gestor_usuarios = GestorDeUsuarios()
    usuario_actual = None
    
    while True:
        if not usuario_actual:
            print("\n1. Iniciar sesión")
            print("2. Registrarse")
            print("3. Salir")
            opcion = input("Seleccione una opción: ")
            
            if opcion == "1":
                email = input("Email: ")
                contraseña = input("Contraseña: ")
                usuario = gestor_usuarios.validar_credenciales(email, contraseña)
                if isinstance(usuario, Usuario):
                    usuario_actual = usuario
                    print(f"Bienvenido, {usuario_actual.nombre}!")
                else:
                    print(usuario)
            
            elif opcion == "2":
                nombre = input("Nombre: ")
                email = input("Email: ")
                contraseña = input("Contraseña: ")
                print(gestor_usuarios.registrar_usuario(nombre, email, contraseña))
            
            elif opcion == "3":
                print("Saliendo del programa...")
                sys.exit()
            
            else:
                print("Opción inválida. Intente nuevamente.")
        
        else:
            gestor = GestorDeContactos()
            print("\nGestor de Contactos")
            print("1. Agregar Contacto")
            print("2. Ver Contactos")
            print("3. Buscar Contacto")
            print("4. Editar Contacto")
            print("5. Eliminar Contacto")
            print("6. Exportar Contactos")
            print("7. Importar Contactos")
            print("8. Cerrar sesión")
            
            option = input("Seleccione una opción: ")
            
            if option == "1":
                nombre = input("Nombre: ")
                telefono = input("Teléfono: ")
                email = input("Email: ")
                categoria = input("Categoría: ")
                try:
                    contacto = Contacto(nombre, email, telefono, categoria)
                    usuario_actual.agregar_contacto(contacto)
                    print("Contacto agregado correctamente.")
                except ValueError as e:
                    print(f"Error: {e}")
            
            elif option == "2":
                contacts = usuario_actual.obtener_contactos()
                if contacts:
                    for contact in contacts:
                        print(contact)
                else:
                    print("No hay contactos registrados.")
            
            elif option == "3":
                nombre = input("Ingrese el nombre a buscar: ")
                resultados = [c for c in usuario_actual.obtener_contactos() if nombre.lower() in c.nombre.lower()]
                if resultados:
                    for contact in resultados:
                        print(contact)
                else:
                    print("No se encontraron contactos.")
            
            elif option == "4":
                print("Funcionalidad de edición no implementada aún.")
            
            elif option == "5":
                email = input("Ingrese el email del contacto a eliminar: ")
                usuario_actual.contactos = [c for c in usuario_actual.obtener_contactos() if c.email != email]
                print("Contacto eliminado correctamente.")
            
            elif option == "6":
                print("Funcionalidad de exportación no implementada aún.")
            
            elif option == "7":
                print("Funcionalidad de importación no implementada aún.")
            
            elif option == "8":
                print("Cerrando sesión...")
                usuario_actual = None
            
            else:
                print("Opción inválida. Intente nuevamente.")

if __name__ == "__main__":
    menu()
