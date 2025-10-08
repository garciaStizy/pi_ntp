import streamlit as st 
import pandas as pd
from datetime import datetime, timedelta

def mostrar_exploracion_datos():
    st.sidebar.info("Explora y analiza los datos disponibles en el sistema.")
    
    # Título principal simple
    st.title("📊 Exploración de Datos")
    st.write("Análisis completo del conjunto de datos de registros horarios")
    try:
        # Cargar datos
        datos = pd.read_csv('registros_horarios_reales.csv')
        # Convertir fechas y calcular horas trabajadas
        datos['fecha'] = pd.to_datetime(datos['fecha'])
        datos['hora_entrada'] = pd.to_datetime(datos['hora_entrada'], format='%H:%M').dt.time
        datos['hora_salida'] = pd.to_datetime(datos['hora_salida'], format='%H:%M').dt.time
        # Calcular horas trabajadas
        def calcular_horas_trabajadas(entrada, salida):
            entrada_dt = datetime.combine(datetime.today(), entrada)
            salida_dt = datetime.combine(datetime.today(), salida)
            if salida_dt < entrada_dt:
                salida_dt += timedelta(days=1)
            return (salida_dt - entrada_dt).total_seconds() / 3600
        
        datos['horas_trabajadas'] = datos.apply(lambda row: calcular_horas_trabajadas(row['hora_entrada'], row['hora_salida']), axis=1)
        datos['mes'] = datos['fecha'].dt.month_name()
        datos['dia_semana'] = datos['fecha'].dt.day_name()
        # Sidebar con opciones de exploración
        st.sidebar.markdown("### 🎯 Opciones de Exploración")
        opcion_exploracion = st.sidebar.selectbox(
            "Selecciona el tipo de análisis:",
            [
                "  Resumen General",
                "🔍 Análisis de Columnas",
                "📈 Estadísticas Descriptivas",
                "🎨 Visualizaciones",
                "🔄 Valores Únicos",
                " 📊 Análisis Temporal",
                "👥 Análisis por Área/Rol",
                "🕐 Análisis de Horarios"
            ]
        )
        
        if opcion_exploracion == "📋 Resumen General":
            mostrar_resumen_general(datos)
        elif opcion_exploracion == "🔍 Análisis de Columnas":
            mostrar_analisis_columnas(datos)
        elif opcion_exploracion == "📈 Estadísticas Descriptivas":
            mostrar_estadisticas_descriptivas(datos)
        elif opcion_exploracion == "🎨 Visualizaciones":
            mostrar_visualizaciones(datos)
        elif opcion_exploracion == "🔄 Valores Únicos":
            mostrar_valores_unicos(datos)
        elif opcion_exploracion == "📊 Análisis Temporal":
            mostrar_analisis_temporal(datos)
        elif opcion_exploracion == "👥 Análisis por Área/Rol":
            mostrar_analisis_area_rol(datos)
        elif opcion_exploracion == "🕐 Análisis de Horarios":
            mostrar_analisis_horarios(datos)
            
    except FileNotFoundError:
        st.error("❌ Error: No se encontró el archivo 'registros_horarios_reales.csv'")
        st.info("📝 Sugerencia: Asegúrate de que el archivo esté en el directorio raíz del proyecto.")
    except Exception as e:
        st.error(f"❌ Error inesperado: {str(e)}")

def mostrar_resumen_general(datos):
    st.header("📋 Resumen General del Dataset")

    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Total de Registros", len(datos))
    with col2:
        st.metric("👥 Empleados Únicos", datos['nombre'].nunique())
    with col3:
        st.metric("🏢 Áreas Diferentes", datos['area'].nunique())
    with col4:
        st.metric("💼 Roles Únicos", datos['rol'].nunique())
    
    st.markdown("---")
    # Vista previa de los datos
    st.subheader("👀 Vista Previa de los Datos")
    col1, col2 = st.columns([3, 1])
    
    with col2:
        num_filas = st.slider("Número de filas a mostrar", 5, 50, 10)
    
    with col1:
        st.dataframe(datos.head(num_filas), use_container_width=True)