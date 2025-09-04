
### Lo que incluye
- Registro de trabajadores con **nombre y cédula**.  
- Inicio de sesión de usuarios con credenciales simples.  
- Registro manual de horas de **entrada** y **salida**.  
- Validación de horarios frente a la hora de entrada oficial (**07:30 AM**).  
- Cálculo automático de minutos de tardanza.  
- Notificación de tardanza al momento del registro.  
- Visualización de registros en consola.  
- Exportación de reportes en **PDF** (detalle y resumen por trabajador).  
- Almacenamiento de datos en un archivo **JSON**.  

### Lo que no incluye (por ahora)
- Integración con bases de datos SQL.  
- Gestión de permisos, vacaciones o ausencias justificadas.  
- Notificaciones por correo electrónico u otros canales.  
- Interfaz gráfica (solo funciona en consola).  
- Control biométrico o por dispositivos externos (huella, tarjetas, etc.).  

### 👷 Trabajador
- Registrarse en el sistema con **nombre y cédula**.
- Iniciar sesión con sus credenciales (nombre + cédula).
- Registrar su **entrada** y **salida** manualmente.
- Recibir una notificación si llega tarde (después de **07:30 AM**).

## 📑 Flujo del Sistema
Menú Principal
--- Sistema de Registro de Horarios ---
1. Registrar trabajador
2. Iniciar sesión
3. Salir

Menú del Trabajador
--- Menú Trabajador ---
1. Registrar Entrada
2. Registrar Salida
3. Salir

Menú del Administrador
--- Menú Administrador ---
1. Ver registros
2. Exportar registros a PDF
3. Registrar hora (admin)
4. Salir
     |
 Resumen por trabajador
| Cédula   | Días Reg. | Tardanzas | Minutos Tarde |
| -------- | --------- | --------- | ------------- |
| 12345678 | 2         | 1         | 15            |

## ⚠️ Validaciones Importantes
El trabajador solo puede iniciar sesión si está registrado.

Las horas deben ingresarse en formato HH:MM (ejemplo: 07:45).

El sistema calcula la tardanza automáticamente comparando con la hora de entrada permitida (07:30 AM).

Todas las acciones quedan guardadas en el archivo db.json.


