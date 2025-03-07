# Resumen de Casos de Prueba

## Requisitos del Sistema

1. El sistema debe permitir la creación, edición, filtrado, exportación e importación de contactos.
2. Los contactos deben incluir al menos un nombre, un número de teléfono, un correo electrónico y una categoría.
3. Los números de teléfono deben ser numéricos y contener un mínimo de 10 dígitos.
4. El correo electrónico debe tener un formato válido.
5. Las categorías deben ser predefinidas o personalizables por el usuario.
6. El sistema debe manejar errores correctamente, mostrando mensajes adecuados en caso de entradas inválidas.
7. La exportación de contactos debe generar archivos en formato .vcf.
8. La importación de contactos debe ser capaz de procesar archivos .vcf válidos y detectar errores en formatos incorrectos.
9. El sistema debe ser capaz de manejar grandes volúmenes de datos sin afectar el rendimiento.

**Tablas de Casos de Prueba**

---
### **Casos de Prueba - Contacto**

| ID  | Caso de Prueba | Entrada | Resultado Esperado | Tipo |
|-----|--------------|---------|--------------------|------|
| C01 | Crear contacto válido | Nombre: Luis, Teléfono: 123456789, Email: luis@correo.com, Categoría: Amigo | Contacto creado exitosamente | Normal |
| C02 | Teléfono muy corto | Nombre: Ana, Teléfono: 123, Email: ana@correo.com, Categoría: Trabajo | InvalidPhoneNumberError | Error |
| C03 | Teléfono con letras | Nombre: Pedro, Teléfono: ABC1234, Email: pedro@correo.com, Categoría: Amigo | InvalidPhoneNumberError | Error |
| C04 | Teléfono muy largo | Nombre: María, Teléfono: 1234567890123456, Email: maria@correo.com, Categoría: Familia | InvalidPhoneNumberError | Extremo |
| C05 | Email sin arroba | Nombre: Carlos, Teléfono: 987654321, Email: carlos.correo.com, Categoría: Trabajo | InvalidEmailError | Error |
| C06 | Email sin punto | Nombre: Juan, Teléfono: 987654321, Email: juan@correocom, Categoría: Familia | InvalidEmailError | Error |
| C07 | Nombre vacío | Nombre: '', Teléfono: 987654321, Email: test@correo.com, Categoría: Trabajo | ContactError | Error |
| C08 | Email vacío | Nombre: Carlos, Teléfono: 987654321, Email: '', Categoría: Trabajo | InvalidEmailError | Error |

---
### **Casos de Prueba - GestorDeContactos**

| ID  | Caso de Prueba | Entrada | Resultado Esperado | Tipo |
|-----|--------------|---------|--------------------|------|
| G01 | Agregar contacto válido | Contacto: Luis | Contacto agregado correctamente | Normal |
| G02 | Agregar contacto duplicado | Contacto: Luis (ya existe) | DuplicateContactError | Error |
| G03 | Editar contacto existente | Nombre: Juan, Nuevo Teléfono: 987654321 | Teléfono actualizado | Normal |
| G04 | Editar contacto inexistente | Nombre: Juan (no existe) | ContactNotFoundError | Error |
| G05 | Editar contacto con email inválido | Nombre: Pedro, Nuevo Email: pedroexample.com | InvalidEmailError | Error |
| G06 | Filtrar contactos por categoría existente | Categoría: Amigo | Lista con contactos filtrados | Normal |
| G07 | Filtrar contactos por categoría inexistente | Categoría: Desconocida | Lista vacía | Extremo |
| G08 | Eliminar contacto existente | Nombre: Luis | Contacto eliminado correctamente | Normal |
| G09 | Eliminar contacto inexistente | Nombre: Carlos (no existe) | ContactNotFoundError | Error |
| G10 | Exportar contactos sin permisos | Archivo: contactos.vcf | VCFExportError | Error |
| G11 | Importar archivo inexistente | Archivo: archivo_invalido.vcf | VCFImportError | Error |

---
### **Casos de Prueba - Usuario**

| ID  | Caso de Prueba | Entrada | Resultado Esperado | Tipo |
|-----|--------------|---------|--------------------|------|
| U01 | Registro con email válido | Nombre: Sara, Email: sara@correo.com, Contraseña: password123 | Usuario registrado correctamente | Normal |
| U02 | Registro con email inválido | Nombre: Sara, Email: saracorreo.com, Contraseña: password123 | InvalidEmailError | Error |
| U03 | Registro con contraseña vacía | Nombre: Sara, Email: sara@correo.com, Contraseña: '' | ContactError | Error |
| U04 | Inicio de sesión exitoso | Email: sara@correo.com, Contraseña: password123 | Inicio de sesión correcto | Normal |
| U05 | Inicio de sesión con contraseña incorrecta | Email: sara@correo.com, Contraseña: incorrecta456 | Inicio de sesión fallido | Error |
| U06 | Inicio de sesión con email en mayúsculas | Email: SARA@CORREO.COM, Contraseña: password123 | Inicio de sesión correcto | Extremo |
| U07 | Inicio de sesión con contraseña vacía | Email: sara@correo.com, Contraseña: '' | Inicio de sesión fallido | Extremo |

---


