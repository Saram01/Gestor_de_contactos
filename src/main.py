import sys
from src.model.gestor_contactos import GestorDeContactos
from src.model.contactos import Contacto

def menu():
    gestor = GestorDeContactos()
    while True:
        print("\nGestor de Contactos")
        print("1. Agregar Contacto")
        print("2. Ver Contactos")
        print("3. Buscar Contacto")
        print("4. Editar Contacto")
        print("5. Eliminar Contacto")
        print("6. Exportar Contactos")
        print("7. Importar Contactos")
        print("8. Salir")
        
        option = input("Seleccione una opción: ")
        
        if option == "1":
            nombre = input("Nombre: ")
            telefono = input("Teléfono: ")
            email = input("Email: ")
            categoria = input("Categoría: ")
            try:
                contacto = Contacto(nombre, email, telefono, categoria)
                print(gestor.agregar_contacto(contacto))
            except ValueError as e:
                print(f"Error: {e}")
        
        elif option == "2":
            contacts = gestor.listar_contactos()
            if isinstance(contacts, list):
                for contact in contacts:
                    print(contact)
            else:
                print(contacts)
        
        elif option == "3":
            nombre = input("Ingrese el nombre a buscar: ")
            resultados = gestor.buscar_contacto(nombre)
            if isinstance(resultados, list):
                for contact in resultados:
                    print(contact)
            else:
                print(resultados)
        
        elif option == "4":
            email = input("Ingrese el email del contacto a editar: ")
            nuevo_telefono = input("Nuevo teléfono (dejar vacío para no cambiar): ")
            nuevo_email = input("Nuevo email (dejar vacío para no cambiar): ")
            nueva_categoria = input("Nueva categoría (dejar vacío para no cambiar): ")
            print(gestor.editar_contacto(email, nuevo_telefono or None, nuevo_email or None, nueva_categoria or None))
        
        elif option == "5":
            email = input("Ingrese el email del contacto a eliminar: ")
            print(gestor.eliminar_contacto(email))
        
        elif option == "6":
            filename = input("Ingrese el nombre del archivo para exportar: ")
            print(gestor.exportar_contactos(filename))
        
        elif option == "7":
            filename = input("Ingrese el nombre del archivo para importar: ")
            print(gestor.importar_contactos(filename))
        
        elif option == "8":
            print("Saliendo del programa...")
            sys.exit()
        
        else:
            print("Opción inválida. Intente nuevamente.")

if __name__ == "__main__":
    menu()
