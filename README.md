# ⏰ Sistema de Registro de Horarios

Este proyecto es una aplicación en **Python** que permite gestionar el registro de horarios de trabajadores y administradores.  
Incluye registro manual de horas de entrada/salida, control de tardanzas y exportación de reportes en **PDF**.

## 📌 Alcance del Proyecto

El sistema fue diseñado para pequeñas y medianas empresas que requieran un control básico de asistencia sin depender de sistemas complejos o costosos.  

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

## 🚀 Funcionalidades
### 👨‍💼 Administrador
- Ver todos los registros de asistencia.
- Registrar horas en nombre de un trabajador.
- Exportar registros a PDF con:
  - **Detalle** de entradas y salidas.
  - **Resumen por trabajador** (días registrados, tardanzas y minutos tarde).

### 👷 Trabajador
- Registrarse en el sistema con **nombre y cédula**.
- Iniciar sesión con sus credenciales (nombre + cédula).
- Registrar su **entrada** y **salida** manualmente.
- Recibir una notificación si llega tarde (después de **07:30 AM**).

## 📂 Estructura del Proyecto

registro_horarios/
│── main.py # Archivo principal (menús y flujo del sistema)
│── services/
│ ├── storage_service.py # Manejo de la base de datos en JSON
│ ├── user_service.py # Registro de trabajadores
│ ├── auth_service.py # Inicio de sesión
│ ├── record_service.py # Lógica de registro de asistencia
│ └── pdf_service.py # Exportación de reportes en PDF
│── db.json # Base de datos (usuarios y registros de asistencia)
│── reportes/ # Carpeta donde se generan los reportes PDF

## 📑 Flujo del Sistema
# 🔹 Menú Principal
--- Sistema de Registro de Horarios ---
1. Registrar trabajador
2. Iniciar sesión
3. Salir

# 🔹 Menú del Trabajador
--- Menú Trabajador ---
1. Registrar Entrada
2. Registrar Salida
3. Salir

# 🔹 Menú del Administrador
--- Menú Administrador ---
1. Ver registros
2. Exportar registros a PDF
3. Registrar hora (admin)
4. Salir

## 📄 Reportes en PDF

| Trabajador   | Fecha      | Entrada | Salida | Tardanza | Observación |
| ------------ | ---------- | ------- | ------ | -------- | ----------- |
| Carlos Perez | 2025-08-17 | 07:45   | 17:10  | 15 min   | Trancones   |
| Carlos Perez | 2025-08-16 | 07:30   | 17:00  | -        | -           |

# 🔹 Resumen por trabajador
| Cédula   | Días Reg. | Tardanzas | Minutos Tarde |
| -------- | --------- | --------- | ------------- |
| 12345678 | 2         | 1         | 15            |

## ✨ Mejoras Futuras

Implementar una interfaz gráfica (GUI) en lugar de consola.

Integrar con una base de datos SQL para mayor escalabilidad.

Enviar notificaciones automáticas al administrador (por correo electrónico).

Implementar permisos/vacaciones para trabajadores.

Exportación a otros formatos (Excel, CSV).

## ⚠️ Validaciones Importantes

El trabajador solo puede iniciar sesión si está registrado.

Las horas deben ingresarse en formato HH:MM (ejemplo: 07:45).

El sistema calcula la tardanza automáticamente comparando con la hora de entrada permitida (07:30 AM).

Todas las acciones quedan guardadas en el archivo db.json.

##  Miembros
- **Nombres:** Samuel Bernal,Cristian Sierra,Harrison Rengifo,Sebastian Garcia,Santiago Puerta
- **Fecha Final:** Finnal de tercer momento 
- **Materia:** Nuevas Tecnologias 

---
