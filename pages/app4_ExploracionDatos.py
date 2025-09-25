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
        st.error("❌ *Error*: No se encontró el archivo 'registros_horarios_reales.csv'")
        st.info("📝 *Sugerencia*: Asegúrate de que el archivo esté en el directorio raíz del proyecto.")
    except Exception as e:
        st.error(f"❌ *Error inesperado*: {str(e)}")

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
        # Información del dataset
    st.subheader("ℹ Información del Dataset")
    
    info_data = {
        'Columna': datos.columns,
        'Tipo de Dato': [str(dtype) for dtype in datos.dtypes],
        'Valores No Nulos': [datos[col].count() for col in datos.columns],
        'Valores Nulos': [datos[col].isnull().sum() for col in datos.columns],
        'Valores Únicos': [datos[col].nunique() for col in datos.columns]
    }
    
    info_df = pd.DataFrame(info_data)
    st.dataframe(info_df, use_container_width=True)

def mostrar_analisis_columnas(datos):
    st.header("🔍 Análisis Detallado por Columnas")
    
    columna_seleccionada = st.selectbox(
        "Selecciona una columna para análisis detallado:",
        datos.columns
    )
    
    st.subheader(f"📊 Análisis de la columna: *{columna_seleccionada}*")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("📈 Estadísticas Básicas:")
        if datos[columna_seleccionada].dtype in ['int64', 'float64']:
            stats = datos[columna_seleccionada].describe()
            st.dataframe(stats.to_frame().T)
        else:
            st.write(f"- *Tipo de dato*: {datos[columna_seleccionada].dtype}")
            st.write(f"- *Valores únicos*: {datos[columna_seleccionada].nunique()}")
            st.write(f"- *Valores nulos*: {datos[columna_seleccionada].isnull().sum()}")
            st.write(f"- *Valores más frecuentes*:")
            top_values = datos[columna_seleccionada].value_counts().head()
            st.dataframe(top_values.to_frame())
    
    with col2:
        st.markdown("🎯 Distribución de Valores:")
        if datos[columna_seleccionada].dtype in ['int64', 'float64']:
            st.subheader(f"Distribución de {columna_seleccionada}")
            st.bar_chart(datos[columna_seleccionada].value_counts())
        else:
            value_counts = datos[columna_seleccionada].value_counts().head(10)
            st.subheader(f"Top 10 valores más frecuentes en {columna_seleccionada}")
            st.bar_chart(value_counts)

def mostrar_estadisticas_descriptivas(datos):
    st.header("📈 Estadísticas Descriptivas Completas")
    # Estadísticas para columnas numéricas
    st.subheader("🔢 Columnas Numéricas")
    columnas_numericas = datos.select_dtypes(include=['int64', 'float64']).columns
    if len(columnas_numericas) > 0:
        st.dataframe(datos[columnas_numericas].describe(), use_container_width=True)
    else:
        st.info("No se encontraron columnas numéricas en el dataset.")
        # Estadísticas para columnas categóricas
    st.subheader("📝 Columnas Categóricas")
    columnas_categoricas = datos.select_dtypes(include=['object']).columns
    
    for col in columnas_categoricas:
        with st.expander(f"📊 Análisis de {col}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("*Estadísticas:*")
                st.write(f"- Valores únicos: {datos[col].nunique()}")
                st.write(f"- Valor más frecuente: {datos[col].mode().iloc[0] if not datos[col].mode().empty else 'N/A'}")
                st.write(f"- Frecuencia del más común: {datos[col].value_counts().iloc[0]}")
            
            with col2:
                st.write("*Top 5 valores más frecuentes:*")
                st.dataframe(datos[col].value_counts().head().to_frame())

def mostrar_visualizaciones(datos):
    st.header("🎨 Visualizaciones Interactivas")
    
    tipo_grafico = st.selectbox(
        "Selecciona el tipo de visualización:",
        [
            "📊 Distribución por Área",
            "👔 Distribución por Rol",
            "📅 Registros por Mes",
            "🕐 Horas Trabajadas"
        ]
    )
    
    if tipo_grafico == "📊 Distribución por Área":
        st.subheader("Distribución de Empleados por Área")
        area_counts = datos['area'].value_counts()
        st.bar_chart(area_counts)
        # Mostrar datos tabulares
        st.subheader("Detalle por Área")
        st.dataframe(area_counts.to_frame('Cantidad'), use_container_width=True)
    
    elif tipo_grafico == "👔 Distribución por Rol":
        st.subheader("Distribución de Empleados por Rol")
        rol_counts = datos['rol'].value_counts()
        st.bar_chart(rol_counts)
# Análisis cruzado área-rol
        st.subheader("Matriz Área vs Rol")
        crosstab = pd.crosstab(datos['area'], datos['rol'])
        st.dataframe(crosstab, use_container_width=True)
    
    elif tipo_grafico == "📅 Registros por Mes":
        st.subheader("Número de Registros por Mes")
        mes_counts = datos['mes'].value_counts()
        st.bar_chart(mes_counts)
    
    elif tipo_grafico == "🕐 Horas Trabajadas":
        st.subheader("Distribución de Horas Trabajadas")
        # Crear histograma manual ya que st.histogram_chart no existe
        horas_bins = pd.cut(datos['horas_trabajadas'], bins=10).value_counts().sort_index()
        st.bar_chart(horas_bins)
        # Estadísticas por área
        st.subheader("Horas Trabajadas por Área")
        horas_por_area = datos.groupby('area')['horas_trabajadas'].agg(['mean', 'sum', 'count']).round(2)
        st.dataframe(horas_por_area, use_container_width=True)

def mostrar_valores_unicos(datos):
    st.header("🔄 Análisis de Valores Únicos")
    
    for columna in datos.columns:
        with st.expander(f"📋 Valores únicos en: *{columna}*"):
            valores_unicos = datos[columna].unique()
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.metric(f"Total de valores únicos", len(valores_unicos))
                # Mostrar algunos valores únicos
                st.write("*Primeros 10 valores:*")
                for i, valor in enumerate(valores_unicos[:10]):
                    st.write(f"{i+1}. {valor}")
                
                if len(valores_unicos) > 10:
                    st.write(f"... y {len(valores_unicos) - 10} más")
            
            with col2:
                if datos[columna].dtype in ['object']:
                    # Frecuencia de valores
                    freq_data = datos[columna].value_counts().head(10)
                    st.write(f"*Frecuencia de valores en {columna}:*")
                    st.bar_chart(freq_data)

def mostrar_analisis_temporal(datos):
    st.header("📊 Análisis Temporal")

    # Tendencia de registros por fecha
    st.subheader("Tendencia de Registros por Fecha")
    registros_por_fecha = datos.groupby('fecha').size()
    st.line_chart(registros_por_fecha)
# Análisis por día de la semana
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Registros por Día de la Semana")
        dia_counts = datos['dia_semana'].value_counts()
        st.bar_chart(dia_counts)
    
    with col2:
        st.subheader("Distribución por Mes")
        mes_counts = datos['mes'].value_counts()
        st.bar_chart(mes_counts)

def mostrar_analisis_area_rol(datos):
    st.header("👥 Análisis por Área y Rol")
# Análisis por área
    st.subheader("🏢 Análisis por Área")
    area_stats = datos.groupby('area').agg({
        'id_usuario': 'count',
        'horas_trabajadas': ['mean', 'sum', 'std']
    }).round(2)
    
    area_stats.columns = ['Total_Registros', 'Promedio_Horas', 'Total_Horas', 'Desv_Std_Horas']
    st.dataframe(area_stats, use_container_width=True)
    # Análisis por rol
    st.subheader("👔 Análisis por Rol")
    rol_stats = datos.groupby('rol').agg({
        'id_usuario': 'count',
        'horas_trabajadas': ['mean', 'sum', 'std']
    }).round(2)
    
    rol_stats.columns = ['Total_Registros', 'Promedio_Horas', 'Total_Horas', 'Desv_Std_Horas']
    st.dataframe(rol_stats, use_container_width=True)
    # Visualización combinada
    st.subheader("Distribución Área → Rol")
    area_rol_counts = datos.groupby(['area', 'rol']).size().reset_index(name='cantidad')
    st.dataframe(area_rol_counts, use_container_width=True)

def mostrar_analisis_horarios(datos):
    st.header("🕐 Análisis Detallado de Horarios")
    # Estadísticas de horas trabajadas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("⏰ Promedio Horas/Día", f"{datos['horas_trabajadas'].mean():.2f}")
    with col2:
        st.metric("📈 Máximo Horas/Día", f"{datos['horas_trabajadas'].max():.2f}")
    with col3:
        st.metric("📉 Mínimo Horas/Día", f"{datos['horas_trabajadas'].min():.2f}")
    with col4:
        st.metric("📊 Desviación Estándar", f"{datos['horas_trabajadas'].std():.2f}")
    
    st.markdown("---")