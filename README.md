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
| C09 | Email muy largo | Nombre: Carlos, Teléfono: 987654321, Email: 'lauraaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa@correo.com', Categoría: Trabajo | InvalidEmailTooLong | Extremo |
| C10 | Email sin dominio valido | Nombre: Sofia, Teléfono: 9876543210, Email: sofia@correo, Categoría: Amigo | InvalidEmailError | error |
| C11 | Nombre solo con espacios | Nombre: "   ", Telefono: 9876543210, Email: espacios@correo.com| ContactError | Error |
| C12 | Contacto sin categoria | Nombre: David, Telefono: 9876543210, Email: david@correo.com, Categoria: "" | ContactError | Error |



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
| G12 | Mismo nombre diferentes datos | Nombre: Daniel, Teléfono: 1234567890, Email: daniel@correo.com, Categoría: Trabajo, Nombre: Daniel, Teléfono: 0987654321, Email: daniel.otro@correo.com, Categoría: Familia | Crear un contacto con mismo nombre | Normal |
| G13 | Exportar contacto error | /ruta/invalida/contactos.vcf | VCFImportError | Error |
| G14 | Importar VCF corrupto | /ruta/invalida/contactos_corruptos.vcf | VCFImportError | Error |
| G15 | Buscar Contacto con telefono invalido | +12-34567890 | InvalidPhoneNumberError | Error |
| G16 | Agregar contacto con nombre excesivo | Nombre: nombre_largo, Telefono: 9876543210, Email: contacto@correo.com, Categoria: Amigo | ContactError | Error |
| G17 | Categoria muy larga | Nombre: Marta, Telefono: 9876543210, Email: marta@correo.com Categoria: A...AA | ContactError | Error |

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
| U08 | Registro con contraseña muy corta | Email: carlos@correo.com, Contraseña: 123 | Contraseña muy corta | Error |
| U09 | Usuario sin email registrado | Email: carlos@correo.com, Contraseña: password123 | El correo no existe | Error |
| U10 | Nombre de usuario invalido | Usuario: J@cob!, Email: jacob@correo.com, Contraseña: password123 | Nombre de usuario invalido | Error |
| U11 | Registro de Email vacio | Email: "  ", Contraseña: password123 | InvalidEmailError | Error |
| U12 | Contraseña de solo espacios | Correo: ana@correo.com, Contraseña: "  " | Contraseña invalida | Error |
| U13 | Inicio de sesion con email vacio | Correo: "", Contraseña: password123 | Correo invalido | Error |
| U14 | Email y contraseña incorrectos | Email: elena@correo.com, Contraseña: password123 | Correo y contraseña incorrectos | Error |
| U15 | Registro con nombre de usuario vacio | Usuario: "", Email: usuario@correo.com, Contraseña: abcd123 | Usuario invalido | Error |

---


