import streamlit as st
import pandas as pd

from pages.app1 import mostrar_horarios
from pages.app2 import mostrar_RegistroEducativos
from pages.app3_IA import mostrar_ia
from pages.app4_ExploracionDatos import mostrar_exploracion_datos

st.set_page_config(
    page_title="Panel Principal - Sistema de Gestión", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .app-card {
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        background-color: #f8f9fa;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .app-title {
        color: #2c3e50;
        font-size: 1.3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .app-description {
        color: #2c3e50;
        font-size: 1.1rem;
        font-weight: 500;
        line-height: 1.6;
        margin-bottom: 1rem;
    }
    .feature-list {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #3498db;
        font-size: 1.05rem;
        font-weight: 500;
        color: #2c3e50;
    }
    .stats-container {
        background: linear-gradient(135deg, #74b9ff, #0984e3);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header principal
st.markdown("""
<div class="main-header">
    <h1>🏢 Inicio de Apps</h1>
    <p>Panel de control unificado para análisis de datos y gestión empresarial</p>
</div>
""", unsafe_allow_html=True)

# Sidebar con información del sistema
st.sidebar.markdown("### 📊 Navegación del Sistema")
st.sidebar.markdown("---")

opcion = st.sidebar.selectbox(
    "🎯 Selecciona una aplicación:",
    (
        "🏠 Inicio",
        "⏰ Registro de Horarios",
        "🎓 Centros Educativos",
        "🤖 Inteligencia Artificial",
        "📈 Exploración de Datos"
    )
)

# Información adicional en sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 📋 Información del Sistema")
st.sidebar.info("🔄 **Estado**: Operativo\n📅 **Última actualización**: Hoy\n👥 **Módulos activos**: 4")

if opcion == "🏠 Inicio":
    # Bienvenida principal
    st.markdown("## 👋 Bienvenido al Inicio de Apps")
    st.markdown("""
    Este sistema integra múltiples herramientas de análisis y gestión empresarial 
    diseñadas para optimizar los procesos organizacionales y facilitar la toma de decisiones.
    """)
    
    st.markdown("---")
    
    # Descripción detallada de cada aplicación
    st.markdown("## 🎯 Módulos del Sistema")
    
    # App 1: Registro de Horarios
    st.markdown("""
    <div class="app-card">
        <div class="app-title">⏰ Aplicación 1: Registro de Horarios</div>
        <div class="app-description">
            Módulo especializado en la gestión y análisis de registros temporales del personal. 
            Permite un control exhaustivo de horarios laborales con capacidades de filtrado avanzado.
        </div>
        <div class="feature-list">
            <strong>🔧 Características principales:</strong><br>
            • Filtrado por persona, área y rol<br>
            • Análisis de rangos de fechas personalizables<br>
            • Cálculo automático de horas trabajadas<br>
            • Visualizaciones estadísticas interactivas<br>
            • Reportes por día, área y rol<br>
            • Interfaz intuitiva con gráficos dinámicos
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # App 2: Centros Educativos
    st.markdown("""
    <div class="app-card">
        <div class="app-title">🎓 Aplicación 2: Centros Educativos</div>
        <div class="app-description">
            Sistema de gestión para instituciones educativas que permite el análisis de infraestructura 
            y distribución geográfica de centros educativos con herramientas de filtrado múltiple.
        </div>
        <div class="feature-list">
            <strong>🔧 Características principales:</strong><br>
            • Filtrado por municipio y categoría educativa<br>
            • Análisis del estado de infraestructura<br>
            • Visualización de distribución geográfica<br>
            • Reportes estadísticos por región<br>
            • Análisis comparativo de categorías<br>
            • Dashboard interactivo con métricas clave
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # App 3: Inteligencia Artificial
    st.markdown("""
    <div class="app-card">
        <div class="app-title">🤖 Aplicación 3: Inteligencia Artificial</div>
        <div class="app-description">
            Interfaz de consulta inteligente que permite interactuar con sistemas de IA avanzados 
            para obtener respuestas y análisis automatizados de datos empresariales.
        </div>
        <div class="feature-list">
            <strong>🔧 Características principales:</strong><br>
            • Consultas en lenguaje natural<br>
            • Respuestas automatizadas inteligentes<br>
            • Integración con APIs de IA<br>
            • Análisis predictivo de datos<br>
            • Interfaz conversacional intuitiva<br>
            • Procesamiento de consultas complejas
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # App 4: Exploración de Datos
    st.markdown("""
    <div class="app-card">
        <div class="app-title">📈 Aplicación 4: Exploración de Datos</div>
        <div class="app-description">
            Herramienta avanzada de análisis exploratorio que permite investigar patrones, 
            tendencias y anomalías en grandes conjuntos de datos empresariales.
        </div>
        <div class="feature-list">
            <strong>🔧 Características principales:</strong><br>
            • Análisis exploratorio automatizado<br>
            • Visualizaciones estadísticas avanzadas<br>
            • Detección de patrones y anomalías<br>
            • Correlaciones entre variables<br>
            • Reportes de calidad de datos<br>
            • Interfaz de análisis interactivo
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Instrucciones de uso
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🚀 Cómo empezar
        1. Selecciona un módulo del menú lateral
        2. Explora las funcionalidades disponibles
        3. Utiliza los filtros para personalizar vistas
        """)
    
    with col2:
        st.markdown("""
        ### 💡 Consejos útiles
        - Usa los filtros para análisis específicos
        - Exporta datos cuando sea necesario
        - Revisa las estadísticas regularmente
        """)
    
    with col3:
        st.markdown("""
        ### 🔗 Navegación
        - Menú lateral para cambiar módulos
        - Botones de acción en cada vista
        - Filtros interactivos disponibles
        """)

elif opcion == "⏰ Registro de Horarios":
    mostrar_horarios()
elif opcion == "🎓 Centros Educativos":
    mostrar_RegistroEducativos()
elif opcion == "🤖 Inteligencia Artificial":
    mostrar_ia()
elif opcion == "📈 Exploración de Datos":
    mostrar_exploracion_datos()

