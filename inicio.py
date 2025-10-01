import streamlit as st
import pandas as pd

from pages.app1 import mostrar_horarios
from pages.app2 import mostrar_RegistroEducativos
from pages.app4_ExploracionDatos import mostrar_exploracion_datos
from pages.app5_ExploracionDatos import mostrar_exploracion_centros_educativos

st.set_page_config(
    page_title="Panel Principal - Sistema de Gestión", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header principal
st.title("🏢 Inicio de Apps")
st.subheader("Panel de control unificado para análisis de datos y gestión empresarial")

# Sidebar con información del sistema
st.sidebar.header("📊 Navegación del Sistema")
st.sidebar.divider()

opcion = st.sidebar.selectbox(
    "🎯 Selecciona una aplicación:",
    (
        "🏠 Inicio",
        "⏰ Registro de Horarios",
        "🎓 Centros Educativos",
        "📈 Exploración de Datos",
        "🏫 Exploración Centros Educativos"
    )
)

# Información adicional en sidebar
st.sidebar.divider()
st.sidebar.subheader("📋 Información del Sistema")
st.sidebar.info("🔄 **Estado**: Operativo\n📅 **Última actualización**: Hoy\n👥 **Módulos activos**: 4")

if opcion == "🏠 Inicio":
    # Bienvenida principal
    st.header("👋 Bienvenido al Inicio de Apps")
    st.write("""
    Este sistema integra múltiples herramientas de análisis y gestión empresarial 
    diseñadas para optimizar los procesos organizacionales y facilitar la toma de decisiones.
    """)
    
    st.divider()
    
    # Descripción detallada de cada aplicación
    st.header("🎯 Módulos del Sistema")
    
    # App 1: Registro de Horarios
    with st.container():
        st.subheader("⏰ Aplicación 1: Registro de Horarios")
        st.write("""
        Módulo especializado en la gestión y análisis de registros temporales del personal. 
        Permite un control exhaustivo de horarios laborales con capacidades de filtrado avanzado.
        """)
        
        with st.expander("🔧 Características principales"):
            st.write("""
            - Filtrado por persona, área y rol
            - Análisis de rangos de fechas personalizables
            - Cálculo automático de horas trabajadas
            - Visualizaciones estadísticas interactivas
            - Reportes por día, área y rol
            - Interfaz intuitiva con gráficos dinámicos
            """)
    
    st.divider()
    
    # App 2: Centros Educativos
    with st.container():
        st.subheader("🎓 Aplicación 2: Centros Educativos")
        st.write("""
        Sistema de gestión para instituciones educativas que permite el análisis de infraestructura 
        y distribución geográfica de centros educativos con herramientas de filtrado múltiple.
        """)
        
        with st.expander("🔧 Características principales"):
            st.write("""
            - Filtrado por municipio y categoría educativa
            - Análisis del estado de infraestructura
            - Visualización de distribución geográfica
            - Reportes estadísticos por región
            - Análisis comparativo de categorías
            - Dashboard interactivo con métricas clave
            """)
    
    st.divider()
    
    # App 3: Exploración de Datos
    with st.container():
        st.subheader("📈 Aplicación 3: Exploración de Datos")
        st.write("""
        Herramienta avanzada de análisis exploratorio que permite investigar patrones, 
        tendencias y anomalías en grandes conjuntos de datos empresariales.
        """)
        
        with st.expander("🔧 Características principales"):
            st.write("""
            - Análisis exploratorio automatizado
            - Visualizaciones estadísticas avanzadas
            - Detección de patrones y anomalías
            - Correlaciones entre variables
            - Reportes de calidad de datos
            - Interfaz de análisis interactivo
            """)
    
    st.divider()
    
    # App 4: Exploración Centros Educativos
    with st.container():
        st.subheader("🏫 Aplicación 4: Exploración Centros Educativos")
        st.write("""
        Módulo especializado en el análisis exploratorio de datos de centros educativos.
        Permite realizar análisis geográficos, de infraestructura y distribuciones detalladas.
        """)
        
        with st.expander("🔧 Características principales"):
            st.write("""
            - Análisis geográfico con mapas interactivos
            - Evaluación del estado de infraestructura
            - Distribuciones por municipio y categoría
            - Estadísticas descriptivas especializadas
            - Visualizaciones de correlaciones geográficas
            - Análisis de concentración educativa
            """)
    
    # Instrucciones de uso
    st.divider()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🚀 Cómo empezar")
        st.write("""
        1. Selecciona un módulo del menú lateral
        2. Explora las funcionalidades disponibles
        3. Utiliza los filtros para personalizar vistas
        """)
    
    with col2:
        st.subheader("💡 Consejos útiles")
        st.write("""
        - Usa los filtros para análisis específicos
        - Exporta datos cuando sea necesario
        - Revisa las estadísticas regularmente
        """)
    
    with col3:
        st.subheader("🔗 Navegación")
        st.write("""
        - Menú lateral para cambiar módulos
        - Botones de acción en cada vista
        - Filtros interactivos disponibles
        """)

elif opcion == "⏰ Registro de Horarios":
    mostrar_horarios()
elif opcion == "🎓 Centros Educativos":
    mostrar_RegistroEducativos()
elif opcion == "📈 Exploración de Datos":
    mostrar_exploracion_datos()
elif opcion == "🏫 Exploración Centros Educativos":
    mostrar_exploracion_centros_educativos()

