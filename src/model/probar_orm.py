# from db import SessionLocal, Usuario

# # Crear una nueva sesión
# db = SessionLocal()

# # Crear un nuevo usuario
# nuevo_usuario = Usuario(nombre_usuario="saritamartinez", contrasena="mi_clave_123")

# # Agregarlo a la sesión y confirmar
# db.add(nuevo_usuario)
# db.commit()
# db.refresh(nuevo_usuario)

# # Mostrar el resultado
# print("Usuario insertado:", nuevo_usuario)

# # Cerrar la sesión
# db.close()



# from db import SessionLocal, Usuario

# # Crear sesión
# db = SessionLocal()

# # Consultar todos los usuarios
# usuarios = db.query(Usuario).all()

# print("Lista de usuarios:")
# for usuario in usuarios:
#     print(usuario)

# db.close()

from model.db import SessionLocal
from model.usuario import Usuario
from model.contactos import Contacto


db = SessionLocal()

# 1. Insertar contacto
nuevo_contacto = Contacto(
    nombre="Elena García",
    categoria="Amigos",
    email="elena@example.com",
    telefono="9991234567",
    usuario_id=1  # Asegúrate que este usuario exista
)
db.add(nuevo_contacto)
db.commit()
print("Contacto insertado:", nuevo_contacto)

# 2. Consultar todos los contactos
contactos = db.query(Contacto).all()
print("Lista de contactos:")
for contacto in contactos:
    print(contacto)

# 3. Eliminar un contacto
contacto_a_eliminar = db.query(Contacto).filter_by(nombre="Elena García").first()
if contacto_a_eliminar:
    db.delete(contacto_a_eliminar)
    db.commit()
    print("Contacto eliminado")

db.close()

