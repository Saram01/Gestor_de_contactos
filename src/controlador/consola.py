import getpass

usuarios = {
    "admin": "1234"
}

contactos = []

def login():
    print("=== Inicio de sesión ===")
    usuario = input("Usuario: ")
    contraseña = getpass.getpass("Contraseña: ")
    if usuario in usuarios and usuarios[usuario] == contraseña:
        print("¡Inicio de sesión exitoso!\n")
        return True
    else:
        print("Usuario o contraseña incorrectos.\n")
        return False

def mostrar_menu():
    print("=== Menú Gestor de Contactos ===")
    print("1. Agregar contacto")
    print("2. Editar contacto")
    print("3. Eliminar contacto")
    print("4. Exportar contactos a VCF")
    print("5. Importar contactos desde VCF")
    print("6. Mostrar contactos")
    print("0. Salir")

def agregar_contacto():
    print("--- Agregar contacto ---")
    nombre = input("Nombre: ")
    categoria = input("Categoría: ")
    email = input("Email: ")
    numero = input("Número: ")
    contacto = {
        "nombre": nombre,
        "categoria": categoria,
        "email": email,
        "numero": numero
    }
    contactos.append(contacto)
    print("Contacto agregado.\n")

def mostrar_contactos():
    if not contactos:
        print("No hay contactos.\n")
        return
    print("--- Lista de Contactos ---")
    for i, c in enumerate(contactos):
        print(f"{i + 1}. {c['nombre']} | {c['categoria']} | {c['email']} | {c['numero']}")
    print()

def editar_contacto():
    mostrar_contactos()
    if not contactos:
        return
    try:
        idx = int(input("Número de contacto a editar: ")) - 1
        if idx < 0 or idx >= len(contactos):
            print("Contacto no válido.\n")
            return
        print("Ingrese nuevos datos (deje vacío para mantener el actual):")
        nombre = input(f"Nombre [{contactos[idx]['nombre']}]: ") or contactos[idx]['nombre']
        categoria = input(f"Categoría [{contactos[idx]['categoria']}]: ") or contactos[idx]['categoria']
        email = input(f"Email [{contactos[idx]['email']}]: ") or contactos[idx]['email']
        numero = input(f"Número [{contactos[idx]['numero']}]: ") or contactos[idx]['numero']
        contactos[idx] = {
            "nombre": nombre,
            "categoria": categoria,
            "email": email,
            "numero": numero
        }
        print("Contacto editado.\n")
    except ValueError:
        print("Entrada inválida.\n")

def eliminar_contacto():
    mostrar_contactos()
    if not contactos:
        return
    try:
        idx = int(input("Número de contacto a eliminar: ")) - 1
        if idx < 0 or idx >= len(contactos):
            print("Contacto no válido.\n")
            return
        contacto = contactos.pop(idx)
        print(f"Contacto {contacto['nombre']} eliminado.\n")
    except ValueError:
        print("Entrada inválida.\n")

def exportar_vcf():
    if not contactos:
        print("No hay contactos para exportar.\n")
        return
    nombre_archivo = input("Nombre archivo para exportar (ejemplo: contactos.vcf): ")
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        for c in contactos:
            f.write("BEGIN:VCARD\n")
            f.write("VERSION:3.0\n")
            f.write(f"N:{c['nombre']}\n")
            f.write(f"CATEGORY:{c['categoria']}\n")
            f.write(f"EMAIL:{c['email']}\n")
            f.write(f"TEL:{c['numero']}\n")
            f.write("END:VCARD\n")
    print(f"Contactos exportados a {nombre_archivo}\n")

def importar_vcf():
    nombre_archivo = input("Nombre archivo VCF para importar: ")
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as f:
            contenido = f.read()
        entradas = contenido.split("BEGIN:VCARD")[1:]  
        for entrada in entradas:
            contacto = {}
            lineas = entrada.strip().split("\n")
            for linea in lineas:
                if linea.startswith("N:"):
                    contacto["nombre"] = linea[2:].strip()
                elif linea.startswith("CATEGORY:"):
                    contacto["categoria"] = linea[9:].strip()
                elif linea.startswith("EMAIL:"):
                    contacto["email"] = linea[6:].strip()
                elif linea.startswith("TEL:"):
                    contacto["numero"] = linea[4:].strip()
            if contacto:
                contactos.append(contacto)
        print(f"Contactos importados desde {nombre_archivo}\n")
    except FileNotFoundError:
        print("Archivo no encontrado.\n")
    except Exception as e:
        print(f"Error al importar: {e}\n")

def main():
    if not login():
        return
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            agregar_contacto()
        elif opcion == "2":
            editar_contacto()
        elif opcion == "3":
            eliminar_contacto()
        elif opcion == "4":
            exportar_vcf()
        elif opcion == "5":
            importar_vcf()
        elif opcion == "6":
            mostrar_contactos()
        elif opcion == "0":
            print("Saliendo del gestor. ¡Hasta luego!")
            break
        else:
            print("Opción no válida.\n")

if __name__ == "__main__":
    main()
