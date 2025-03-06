# Resumen de Casos de Prueba

## Requisitos del Sistema

1. El sistema debe permitir la creación, edición, filtrado, exportación e importación de contactos.
2. Los contactos deben incluir al menos un nombre, un número de teléfono, un correo electrónico y una categoría.
3. Los números de teléfono deben ser numéricos y contener un mínimo de 7 dígitos.
4. El correo electrónico debe tener un formato válido.
5. Las categorías deben ser predefinidas o personalizables por el usuario.
6. El sistema debe manejar errores correctamente, mostrando mensajes adecuados en caso de entradas inválidas.
7. La exportación de contactos debe generar archivos en formato .vcf.
8. La importación de contactos debe ser capaz de procesar archivos .vcf válidos y detectar errores en formatos incorrectos.
9. El sistema debe ser capaz de manejar grandes volúmenes de datos sin afectar el rendimiento.

## Casos de Prueba

### Caso de prueba #1: Creación de contacto - Caso normal
| Nombre  | Teléfono   | Email               | Categoría |
|---------|-----------|---------------------|-----------|
| Luis    | 123123123 | luis@example.com   | Familia   |
| Carlos  | 456456456 | carlos@example.com | Amigo     |

### Caso de prueba #2: Creación de contacto - Errores
| Nombre  | Teléfono | Email | Categoría | Resultado Esperado |
|---------|----------|-------|-----------|--------------------|
| ""      | 0        | ""    | ""        | ValueError        |
| Pedro   | 0        | pedro@example.com | Trabajo | ValueError |
| Maria   | 999888777 | ""   | Familia   | ValueError        |

### Caso de prueba #3: Creación de contacto - Casos extremos
| Nombre  | Teléfono        | Email               | Categoría | Resultado Esperado |
|---------|----------------|---------------------|-----------|--------------------|
| NombreLargo x10 | 999999999999 | correo@ejemplo.com | Amigo | Éxito |
| 1500 contactos generados dinámicamente | - | - | - | Todos creados exitosamente |

### Caso de prueba #4: Edición de contacto - Caso normal
| Nombre  | Modificación           | Resultado Esperado |
|---------|------------------------|--------------------|
| Juan    | Teléfono = 111111111   | Éxito |
| Juan    | Email = nuevo@example.com | Éxito |
| Juan    | Categoría = Trabajo    | Éxito |

### Caso de prueba #5: Edición de contacto - Errores
| Nombre   | Modificación         | Resultado Esperado |
|----------|----------------------|--------------------|
| NoExiste | Teléfono = 111111111 | KeyError |
| Juan     | Teléfono = 0         | ValueError |

### Caso de prueba #6: Edición de contacto - Casos extremos
| Nombre  | Modificación                   | Resultado Esperado |
|---------|--------------------------------|--------------------|
| Juan    | Teléfono = 999999999999       | Éxito |
| Juan    | Modificar 150 veces el teléfono | Todos los cambios exitosos |

### Caso de prueba #7: Filtrado de contactos
| Filtro   | Resultado Esperado |
|----------|--------------------|
| Familia  | Lista con 1 contacto |
| Trabajo  | Lista con 1 contacto |
| Amigo    | Lista con 1 contacto |
| NoExiste | Lista vacía |
| ""       | Lista vacía |
| Amigo (con 1500 contactos creados) | Lista con 1500 contactos |
| Familia (sin contactos creados) | Lista vacía |

### Caso de prueba #8: Exportación e importación de contactos
| Acción                  | Entrada                        | Resultado Esperado |
|-------------------------|--------------------------------|--------------------|
| Exportar contactos     | Contactos existentes           | Archivo .vcf generado |
| Exportar contactos     | Múltiples contactos            | Archivo .vcf generado |
| Exportar sin contactos | -                              | Archivo vacío o error |
| Exportar sin permisos  | -                              | Error |
| Exportar 10,000 contactos | -                          | Archivo .vcf grande |
| Exportar con emojis    | -                              | Archivo .vcf generado |
| Importar archivo válido | Archivo .vcf con contactos    | Contactos importados |
| Importar archivo vacío  | Archivo vacío                 | Error o sin cambios |
| Importar archivo inválido | Formato incorrecto         | Error |
| Importar 10,000 contactos | Archivo grande             | Todos importados |
| Importar con caracteres extraños | -                  | Contactos importados |

**Total de Pruebas: 54**

