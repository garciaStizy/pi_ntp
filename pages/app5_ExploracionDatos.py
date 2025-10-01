import streamlit as st 
import pandas as pd

def mostrar_exploracion_centros_educativos():
    st.sidebar.info("Explora y analiza los datos de centros educativos disponibles.")
    
    # Título principal
    st.title("📊 Exploración de Datos - Centros Educativos")
    st.write("Análisis completo del conjunto de datos de centros educativos")
    
    try:
        # Cargar datos
        datos = pd.read_csv('WL_T_Centros_Educativos.csv')
        
        # Sidebar con opciones de exploración
        st.sidebar.header("🎯 Opciones de Exploración")
        opcion_exploracion = st.sidebar.selectbox(
            "Selecciona el tipo de análisis:",
            [
                "📋 Resumen General",
                "🔍 Análisis de Columnas",
                "📈 Estadísticas Descriptivas", 
                "🎨 Visualizaciones",
                "🌍 Análisis Geográfico",
                "🏗️ Análisis de Infraestructura",
                "📊 Distribuciones"
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
        elif opcion_exploracion == "🌍 Análisis Geográfico":
            mostrar_analisis_geografico(datos)
        elif opcion_exploracion == "🏗️ Análisis de Infraestructura":
            mostrar_analisis_infraestructura(datos)
        elif opcion_exploracion == "📊 Distribuciones":
            mostrar_distribuciones(datos)
            
    except FileNotFoundError:
        st.error("❌ Error: No se pudo encontrar el archivo 'WL_T_Centros_Educativos.csv'")
        st.info("📝 *Sugerencia*: Asegúrate de que el archivo esté en el directorio raíz del proyecto.")

def mostrar_resumen_general(datos):
    st.header("📋 Resumen General del Dataset")
    
    # Información básica
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Total de Registros", len(datos))
    
    with col2:
        st.metric("📝 Total de Columnas", len(datos.columns))
    
    with col3:
        st.metric("🏫 Centros Educativos", datos['ESTABLECIMIENTO_EDUCATIVO'].nunique())
    
    with col4:
        st.metric("🏛️ Municipios", datos['MUNICIPIO'].nunique())
    
    st.divider()
    
    # Vista previa de los datos
    st.subheader("👀 Vista Previa de los Datos")
    st.dataframe(datos.head(10))
    
    st.divider()
    
    # Información sobre tipos de datos
    st.subheader("📊 Información de Columnas")
    info_df = pd.DataFrame({
        'Columna': datos.columns,
        'Tipo de Dato': datos.dtypes.astype(str),
        'Valores No Nulos': datos.count(),
        'Valores Nulos': datos.isnull().sum(),
        '% Nulos': (datos.isnull().sum() / len(datos) * 100).round(2)
    })
    st.dataframe(info_df)

def mostrar_analisis_columnas(datos):
    st.header("🔍 Análisis Detallado por Columnas")
    
    # Selector de columna
    columna_seleccionada = st.selectbox(
        "Selecciona una columna para analizar:",
        datos.columns
    )
    
    if columna_seleccionada:
        col = datos[columna_seleccionada]
        
        # Información básica de la columna
        st.subheader(f"Análisis de: {columna_seleccionada}")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total de Valores", len(col))
        
        with col2:
            st.metric("Valores Únicos", col.nunique())
        
        with col3:
            st.metric("Valores Nulos", col.isnull().sum())
        
        with col4:
            st.metric("% Completitud", f"{((len(col) - col.isnull().sum()) / len(col) * 100):.1f}%")
        
        # Análisis específico según el tipo de dato
        if col.dtype == 'object':
            st.subheader("📊 Valores más frecuentes")
            value_counts = col.value_counts().head(10)
            st.bar_chart(value_counts)
            
            with st.expander("Ver tabla de frecuencias"):
                freq_df = pd.DataFrame({
                    'Valor': value_counts.index,
                    'Frecuencia': value_counts.values,
                    'Porcentaje': (value_counts.values / len(col) * 100).round(2)
                })
                st.dataframe(freq_df)
        
        elif pd.api.types.is_numeric_dtype(col):
            st.subheader("📈 Estadísticas Numéricas")
            stats_df = pd.DataFrame({
                'Estadística': ['Media', 'Mediana', 'Moda', 'Desv. Estándar', 'Mínimo', 'Máximo'],
                'Valor': [
                    col.mean(),
                    col.median(),
                    col.mode().iloc[0] if not col.mode().empty else 'N/A',
                    col.std(),
                    col.min(),
                    col.max()
                ]
            })
            st.dataframe(stats_df)
            
            # Histograma
            st.subheader("📊 Distribución")
            st.hist_chart(col.dropna())

def mostrar_estadisticas_descriptivas(datos):
    st.header("📈 Estadísticas Descriptivas")
    
    # Estadísticas de variables categóricas principales
    st.subheader("🏛️ Distribución por Municipio")
    municipio_stats = datos['MUNICIPIO'].value_counts()
    col1, col2 = st.columns(2)
    
    with col1:
        st.bar_chart(municipio_stats)
    
    with col2:
        st.write("**Top 5 Municipios:**")
        for i, (municipio, count) in enumerate(municipio_stats.head().items(), 1):
            st.write(f"{i}. {municipio}: {count} centros")
    
    st.divider()
    
    st.subheader("🎓 Distribución por Categoría")
    categoria_stats = datos['CATEGORIA'].value_counts()
    col1, col2 = st.columns(2)
    
    with col1:
        st.bar_chart(categoria_stats)
    
    with col2:
        st.write("**Distribución por Categoría:**")
        for categoria, count in categoria_stats.items():
            percentage = (count / len(datos) * 100)
            st.write(f"• {categoria}: {count} ({percentage:.1f}%)")
    
    st.divider()
    
    st.subheader("🏗️ Estado de Infraestructura")
    infra_stats = datos['Estado_InfraestructuraE'].value_counts()
    col1, col2 = st.columns(2)
    
    with col1:
        st.bar_chart(infra_stats)
    
    with col2:
        st.write("**Estado de Infraestructura:**")
        for estado, count in infra_stats.items():
            percentage = (count / len(datos) * 100)
            if estado == 'Deficit':
                st.error(f"🔴 {estado}: {count} ({percentage:.1f}%)")
            elif estado == 'Alerta':
                st.warning(f"🟡 {estado}: {count} ({percentage:.1f}%)")
            else:
                st.success(f"🟢 {estado}: {count} ({percentage:.1f}%)")

def mostrar_visualizaciones(datos):
    st.header("🎨 Visualizaciones Avanzadas")
    
    # Gráfico de correlación entre zona y categoría
    st.subheader("🌍 Distribución Zona vs Categoría")
    zona_categoria = pd.crosstab(datos['Zona'], datos['CATEGORIA'])
    st.bar_chart(zona_categoria)
    
    st.divider()
    
    # Análisis por provincia
    st.subheader("🗺️ Centros por Provincia")
    provincia_counts = datos['PROVINCIA'].value_counts()
    st.bar_chart(provincia_counts)
    
    # Mostrar métricas por provincia
    col1, col2, col3 = st.columns(3)
    provincias = datos['PROVINCIA'].unique()
    
    for i, provincia in enumerate(provincias):
        with [col1, col2, col3][i % 3]:
            count = provincia_counts[provincia]
            st.metric(f"📍 {provincia}", f"{count} centros")
    
    st.divider()
    
    # Análisis de establecimientos educativos
    st.subheader("🏫 Top 10 Establecimientos Educativos")
    establecimiento_counts = datos['ESTABLECIMIENTO_EDUCATIVO'].value_counts().head(10)
    st.bar_chart(establecimiento_counts)

def mostrar_analisis_geografico(datos):
    st.header("🌍 Análisis Geográfico")
    
    # Filtros geográficos
    st.subheader("🔍 Filtros Geográficos")
    col1, col2 = st.columns(2)
    
    with col1:
        municipios_selected = st.multiselect(
            "Seleccionar Municipios:",
            datos['MUNICIPIO'].unique(),
            default=datos['MUNICIPIO'].unique()[:3]
        )
    
    with col2:
        provincias_selected = st.multiselect(
            "Seleccionar Provincias:",
            datos['PROVINCIA'].unique(),
            default=datos['PROVINCIA'].unique()
        )
    
    # Filtrar datos
    datos_filtrados = datos[
        (datos['MUNICIPIO'].isin(municipios_selected)) &
        (datos['PROVINCIA'].isin(provincias_selected))
    ]
    
    st.subheader(f"📊 Análisis de {len(datos_filtrados)} centros educativos")
    
    # Coordenadas geográficas
    if 'X' in datos.columns and 'Y' in datos.columns:
        st.subheader("📍 Distribución Geográfica")
        
        # Crear un mapa simple con las coordenadas
        coord_data = datos_filtrados[['Y', 'X']].dropna()
        if not coord_data.empty:
            # Renombrar columnas para que Streamlit las reconozca como lat/lon
            coord_data.columns = ['lat', 'lon']
            st.map(coord_data)
        else:
            st.warning("No hay datos de coordenadas válidos para mostrar el mapa.")
    
    # Estadísticas por zona
    st.subheader("🏙️ Distribución Urbana vs Rural")
    zona_counts = datos_filtrados['Zona'].value_counts()
    col1, col2 = st.columns(2)
    
    with col1:
        st.bar_chart(zona_counts)
    
    with col2:
        for zona, count in zona_counts.items():
            percentage = (count / len(datos_filtrados) * 100)
            if zona == 'URBANA':
                st.info(f"🏙️ {zona}: {count} ({percentage:.1f}%)")
            else:
                st.success(f"🌱 {zona}: {count} ({percentage:.1f}%)")

def mostrar_analisis_infraestructura(datos):
    st.header("🏗️ Análisis de Infraestructura")
    
    # Estado general de infraestructura
    st.subheader("📊 Estado General de Infraestructura")
    
    infra_counts = datos['Estado_InfraestructuraE'].value_counts()
    total_centros = len(datos)
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        deficit_count = infra_counts.get('Deficit', 0)
        st.metric(
            "🔴 En Déficit", 
            deficit_count,
            delta=f"{(deficit_count/total_centros*100):.1f}%"
        )
    
    with col2:
        alerta_count = infra_counts.get('Alerta', 0)
        st.metric(
            "🟡 En Alerta", 
            alerta_count,
            delta=f"{(alerta_count/total_centros*100):.1f}%"
        )
    
    with col3:
        cumple_count = infra_counts.get('Cumple', 0)
        st.metric(
            "🟢 Cumple", 
            cumple_count,
            delta=f"{(cumple_count/total_centros*100):.1f}%"
        )
    
    with col4:
        st.metric("📊 Total Evaluado", total_centros)
    
    st.divider()
    
    # Análisis por municipio
    st.subheader("🏛️ Estado de Infraestructura por Municipio")
    municipio_infra = pd.crosstab(datos['MUNICIPIO'], datos['Estado_InfraestructuraE'])
    st.bar_chart(municipio_infra)
    
    # Tabla detallada
    with st.expander("Ver tabla detallada por municipio"):
        # Calcular porcentajes
        municipio_infra_pct = pd.crosstab(datos['MUNICIPIO'], datos['Estado_InfraestructuraE'], normalize='index') * 100
        municipio_infra_pct = municipio_infra_pct.round(1)
        st.dataframe(municipio_infra_pct)
    
    st.divider()
    
    # Análisis por categoría educativa
    st.subheader("🎓 Estado de Infraestructura por Categoría")
    categoria_infra = pd.crosstab(datos['CATEGORIA'], datos['Estado_InfraestructuraE'])
    st.bar_chart(categoria_infra)

def mostrar_distribuciones(datos):
    st.header("📊 Análisis de Distribuciones")
    
    # Selector de variable para analizar
    st.subheader("🔍 Seleccionar Variable a Analizar")
    
    variables_categoricas = [
        'MUNICIPIO', 'CATEGORIA', 'Estado_InfraestructuraE', 
        'PROVINCIA', 'Zona', 'ESTABLECIMIENTO_EDUCATIVO'
    ]
    
    variable_seleccionada = st.selectbox(
        "Selecciona una variable categórica:",
        variables_categoricas
    )
    
    if variable_seleccionada:
        st.subheader(f"📈 Distribución de: {variable_seleccionada}")
        
        # Calcular distribución
        distribucion = datos[variable_seleccionada].value_counts()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.bar_chart(distribucion)
        
        with col2:
            # Tabla con estadísticas
            st.write("**Estadísticas de Distribución:**")
            for valor, count in distribucion.head(10).items():
                percentage = (count / len(datos) * 100)
                st.write(f"• {valor}: {count} ({percentage:.1f}%)")
            
            if len(distribucion) > 10:
                st.write(f"... y {len(distribucion) - 10} categorías más")
    
    st.divider()
    
    # Análisis de concentración
    st.subheader("📊 Análisis de Concentración")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Índice de concentración por municipio
        municipio_dist = datos['MUNICIPIO'].value_counts()
        municipio_hhi = ((municipio_dist / municipio_dist.sum()) ** 2).sum()
        st.metric(
            "🏛️ Concentración Municipal", 
            f"{municipio_hhi:.3f}",
            help="Índice Herfindahl-Hirschman (0=muy disperso, 1=muy concentrado)"
        )
    
    with col2:
        # Concentración por categoría
        categoria_dist = datos['CATEGORIA'].value_counts()
        categoria_hhi = ((categoria_dist / categoria_dist.sum()) ** 2).sum()
        st.metric(
            "🎓 Concentración por Categoría", 
            f"{categoria_hhi:.3f}"
        )
    
    with col3:
        # Concentración por estado de infraestructura
        infra_dist = datos['Estado_InfraestructuraE'].value_counts()
        infra_hhi = ((infra_dist / infra_dist.sum()) ** 2).sum()
        st.metric(
            "🏗️ Concentración Infraestructura", 
            f"{infra_hhi:.3f}"
        )
