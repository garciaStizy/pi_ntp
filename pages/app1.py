import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta


def cargar_datos_api():
    """Cargar datos desde la API y procesarlos correctamente"""
    try:
        # Realizar petición GET a la API
        response = requests.get('https://68de838bd7b591b4b78fce39.mockapi.io/Horarios')

        if response.status_code == 200:
            # Convertir la respuesta JSON a DataFrame
            data = response.json()
            df = pd.DataFrame(data)
            
            # Limpiar datos nulos o vacíos
            df = df.dropna(subset=['nombre', 'fecha', 'hora_entrada', 'hora_salida'])
            
            # Convertir la columna fecha correctamente
            df['fecha'] = pd.to_datetime(df['fecha'], format='%Y-%m-%d', errors='coerce')
            
            # Eliminar filas con fechas inválidas
            df = df.dropna(subset=['fecha'])
            
            # Agregar columna de duración calculada
            try:
                # Convertir horas a datetime para calcular duración
                df['hora_entrada_dt'] = pd.to_datetime(df['hora_entrada'], format='%H:%M', errors='coerce')
                df['hora_salida_dt'] = pd.to_datetime(df['hora_salida'], format='%H:%M', errors='coerce')
                
                # Eliminar filas con horas inválidas
                df = df.dropna(subset=['hora_entrada_dt', 'hora_salida_dt'])
                
                # Calcular duración en horas
                df['duracion_horas'] = (df['hora_salida_dt'] - df['hora_entrada_dt']).dt.total_seconds() / 3600
                
                # Manejar casos donde la salida es al día siguiente (duración negativa)
                df.loc[df['duracion_horas'] < 0, 'duracion_horas'] += 24
                
            except Exception as e:
                st.warning(f"Error calculando duración: {e}")
                df['duracion_horas'] = 8.0  # Valor por defecto

            # Limpiar columnas de texto
            for col in ['nombre', 'area', 'rol']:
                if col in df.columns:
                    df[col] = df[col].astype(str).str.strip()
            
            return df
        else:
            st.error(f"Error en la petición: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error al cargar datos de la API: {e}")
        return None

    
def mostrar_horarios():
    st.sidebar.info("Visualiza los registros de horarios cargados en el sistema.")
    try:
        datos = cargar_datos_api()
        
        if datos is None or datos.empty:
            st.error("No se pudieron cargar los datos de la API o no hay datos disponibles.")
            return
        
        st.title("📋 Registro de Horarios ⏰")
        
        # Información sobre la aplicación
        with st.expander("ℹ️ ¿Qué es esta aplicación?", expanded=False):
            st.markdown("""
            ### 🎯 **Propósito de la Aplicación**
            Esta aplicación permite **visualizar y analizar los registros de horarios laborales** de empleados 
            obtenidos desde una API externa en tiempo real.
            
            ### 🔧 **Funcionalidades principales:**
            - 📊 **Análisis de horarios**: Visualiza patrones de entrada y salida
            - 👥 **Gestión por personas**: Filtra por empleados específicos
            - 🏢 **Análisis por áreas**: Compara rendimiento entre diferentes zonas
            - 📅 **Filtros temporales**: Analiza períodos específicos
            - ⏱️ **Cálculo automático**: Duración de jornadas laborales
            - 📈 **Métricas clave**: Estadísticas de productividad
            
            ### 👨‍💼 **¿Para quién es útil?**
            - **Supervisores** que necesitan monitorear asistencia
            - **Recursos Humanos** para análisis de horarios
            - **Gerentes** que buscan optimizar turnos
            - **Analistas** de datos laborales
            """)
        
        st.success(f"✅ **Datos cargados correctamente**: {len(datos)} registros desde la API")
        
        # Información rápida sobre los datos
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.info(f"👥 **{datos['nombre'].nunique()}** Empleados")
        with col2:
            st.info(f"🏢 **{datos['area'].nunique()}** Áreas")
        with col3:
            st.info(f"🎭 **{datos['rol'].nunique()}** Roles")
        with col4:
            fecha_range = f"{datos['fecha'].min().strftime('%d/%m/%Y')} - {datos['fecha'].max().strftime('%d/%m/%Y')}"
            st.info(f"📅 **Período**: {fecha_range}")
        
        st.divider()

        # Información sobre filtros
        st.sidebar.markdown("### 🔍 **Panel de Filtros**")
        st.sidebar.markdown("*Usa estos filtros para personalizar tu análisis*")
        
        # Filtro por nombre
        nombres = datos['nombre'].unique()
        nombre_sel = st.sidebar.selectbox(
            "👤 Filtrar por persona", 
            options=['Todos'] + list(nombres),
            help="Selecciona una persona específica para ver solo sus registros"
        )

        # Filtro múltiple por área
        areas = datos['area'].unique()
        areas_sel = st.sidebar.multiselect(
            "🏢 Filtrar por área(s)", 
            options=areas, 
            default=[],
            help="Selecciona una o varias áreas para comparar"
        )

        # Filtro múltiple por rol
        roles = datos['rol'].unique()
        roles_sel = st.sidebar.multiselect(
            "🎭 Filtrar por rol(es)", 
            options=roles, 
            default=[],
            help="Filtra por tipo de trabajo o posición"
        )

        # Filtro por rango de fechas
        fecha_min = datos['fecha'].min().date()
        fecha_max = datos['fecha'].max().date()
        fecha_inicio, fecha_fin = st.sidebar.date_input(
            "📅 Filtrar por rango de fechas",
            value=(fecha_min, fecha_max),
            min_value=fecha_min,
            max_value=fecha_max,
            help="Define el período de tiempo que quieres analizar"
        )

        # Filtro por días de la semana
        dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        dias_seleccionados = st.sidebar.multiselect(
            "📆 Filtrar por días de la semana",
            options=dias_semana,
            default=[],
            help="Selecciona qué días de la semana incluir en el análisis (vacío = todos los días)"
        )

        # Filtro de nivel de productividad
        nivel_productividad = st.sidebar.selectbox(
            "⚡ Nivel de productividad",
            options=['Todos', 'Alto (>10h)', 'Normal (7-10h)', 'Bajo (<7h)'],
            help="Clasifica empleados según horas trabajadas por jornada"
        )

        # Filtro por hora de entrada (solo hora, no minutos)
        try:
            # Filtrar valores no nulos antes de convertir
            horas_validas = datos['hora_entrada'].dropna()
            if len(horas_validas) > 0:
                horas_entrada = horas_validas.str[:2].astype(int)
                hora_min = int(horas_entrada.min())
                hora_max = int(horas_entrada.max())
                hora_entrada_rango = st.sidebar.slider(
                    "⏰ Filtrar por hora de entrada",
                    min_value=hora_min, max_value=hora_max,
                    value=(hora_min, hora_max),
                    help="Ajusta el rango de horas de entrada que te interesa analizar"
                )
            else:
                hora_entrada_rango = (0, 23)
        except Exception as e:
            st.warning(f"Error procesando horas de entrada: {e}")
            hora_entrada_rango = (0, 23)

        # Aplicar filtros
        datos_filtrados = datos.copy()
        if nombre_sel != 'Todos':
            datos_filtrados = datos_filtrados[datos_filtrados['nombre'] == nombre_sel]
        if areas_sel:
            datos_filtrados = datos_filtrados[datos_filtrados['area'].isin(areas_sel)]
        if roles_sel:
            datos_filtrados = datos_filtrados[datos_filtrados['rol'].isin(roles_sel)]
        datos_filtrados = datos_filtrados[
            (datos_filtrados['fecha'].dt.date >= fecha_inicio) &
            (datos_filtrados['fecha'].dt.date <= fecha_fin)
        ]
        # Filtrar por hora de entrada manejando valores nulos
        try:
            mask_hora = datos_filtrados['hora_entrada'].notna()
            if mask_hora.any():
                horas_filtro = datos_filtrados.loc[mask_hora, 'hora_entrada'].str[:2].astype(int)
                mask_rango = horas_filtro.between(hora_entrada_rango[0], hora_entrada_rango[1])
                datos_filtrados = datos_filtrados[mask_hora & mask_rango]
        except Exception as e:
            st.warning(f"Error aplicando filtro de horas: {e}")

        # Filtrar por días de la semana (solo si hay días específicamente seleccionados)
        if dias_seleccionados:
            # Mapear días en español a números (Monday=0, Sunday=6)
            mapeo_dias = {
                'Lunes': 0, 'Martes': 1, 'Miércoles': 2, 'Jueves': 3, 
                'Viernes': 4, 'Sábado': 5, 'Domingo': 6
            }
            dias_numeros = [mapeo_dias[dia] for dia in dias_seleccionados]
            datos_filtrados = datos_filtrados[datos_filtrados['fecha'].dt.dayofweek.isin(dias_numeros)]

        # Filtrar por nivel de productividad
        if nivel_productividad != 'Todos' and 'duracion_horas' in datos_filtrados.columns:
            if nivel_productividad == 'Alto (>10h)':
                datos_filtrados = datos_filtrados[datos_filtrados['duracion_horas'] > 10]
            elif nivel_productividad == 'Normal (7-10h)':
                datos_filtrados = datos_filtrados[
                    (datos_filtrados['duracion_horas'] >= 7) & 
                    (datos_filtrados['duracion_horas'] <= 10)
                ]
            elif nivel_productividad == 'Bajo (<7h)':
                datos_filtrados = datos_filtrados[datos_filtrados['duracion_horas'] < 7]

        st.sidebar.divider()
        st.sidebar.markdown("### 🏆 **Filtros Especiales**")
        
        # Filtro: mostrar solo la persona con más horas trabajadas
        filtro_max_horas = st.sidebar.checkbox(
            "🥇 Mostrar solo el empleado con más horas", 
            value=False,
            help="Identifica automáticamente al empleado más productivo"
        )
        if filtro_max_horas and 'duracion_horas' in datos_filtrados.columns and 'nombre' in datos_filtrados.columns:
            suma_horas = datos_filtrados.groupby('nombre')['duracion_horas'].sum()
            persona_max = suma_horas.idxmax()
            datos_filtrados = datos_filtrados[datos_filtrados['nombre'] == persona_max]

        # Mostrar información de filtros aplicados
        filtros_activos = []
        if nombre_sel != 'Todos':
            filtros_activos.append(f"👤 {nombre_sel}")
        if areas_sel:
            filtros_activos.append(f"🏢 {len(areas_sel)} área(s)")
        if roles_sel:
            filtros_activos.append(f"🎭 {len(roles_sel)} rol(es)")
        if dias_seleccionados:  # Solo mostrar si hay días específicamente seleccionados
            filtros_activos.append(f"📆 {len(dias_seleccionados)} día(s) específico(s)")
        if nivel_productividad != 'Todos':
            filtros_activos.append(f"⚡ {nivel_productividad}")
        if filtro_max_horas:
            filtros_activos.append("🥇 Top performer")
        
        if len(datos_filtrados) != len(datos):
            filtros_texto = " • ".join(filtros_activos) if filtros_activos else "Filtros aplicados"
            st.info(f"🔍 **{filtros_texto}**: Mostrando {len(datos_filtrados)} de {len(datos)} registros totales")
        
        st.subheader("📋 Registros Filtrados")
        st.caption("*Tabla con los datos que coinciden con tus filtros (máximo 50 registros)*")
        
        # Preparar datos para mostrar (sin las columnas técnicas)
        datos_mostrar = datos_filtrados[['nombre', 'fecha', 'hora_entrada', 'hora_salida', 'area', 'rol', 'duracion_horas']].head(50)
        datos_mostrar['fecha'] = datos_mostrar['fecha'].dt.strftime('%d/%m/%Y')
        datos_mostrar['duracion_horas'] = datos_mostrar['duracion_horas'].round(2)
        datos_mostrar.columns = ['Nombre', 'Fecha', 'Entrada', 'Salida', 'Área', 'Rol', 'Horas Trabajadas']
        
        st.dataframe(datos_mostrar, use_container_width=True)

        # Estadísticas generales
        st.subheader("📊 Estadísticas Generales")
        if len(datos_filtrados) > 0:
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**📈 Total de registros**: {len(datos_filtrados)}")
                st.write(f"**👥 Empleados únicos**: {datos_filtrados['nombre'].nunique()}")
            with col2:
                st.write(f"**🏢 Áreas involucradas**: {datos_filtrados['area'].nunique()}")
                st.write(f"**🎭 Roles diferentes**: {datos_filtrados['rol'].nunique()}")
        else:
            st.warning("⚠️ No hay registros que coincidan con los filtros seleccionados")
        # Gráfico 1: Promedio de horas trabajadas por persona
        if 'duracion_horas' in datos_filtrados.columns and 'nombre' in datos_filtrados.columns and len(datos_filtrados) > 0:
            st.write(f"**⏱️ Promedio general de horas trabajadas**: {datos_filtrados['duracion_horas'].mean():.2f} horas por jornada")
            duracion_prom = datos_filtrados.groupby('nombre')['duracion_horas'].mean()
            st.subheader("👥 Promedio de Horas Trabajadas por Persona")
            st.caption("*Este gráfico muestra cuántas horas promedio trabaja cada empleado por jornada*")
            st.bar_chart(duracion_prom)

        # Gráfico 2: Registros por área
        if 'area' in datos_filtrados.columns and len(datos_filtrados) > 0:
            area_df = datos_filtrados['area'].value_counts().rename_axis('Área').reset_index(name='Cantidad')
            area_df.set_index('Área', inplace=True)
            st.subheader("🏢 Actividad por Área de Trabajo")
            st.caption("*Número total de registros de horarios por cada área*")
            st.bar_chart(area_df)

        # Gráfico 3: Tendencia de asistencia diaria (gráfico de líneas)
        if 'fecha' in datos_filtrados.columns and len(datos_filtrados) > 0:
            # Preparar datos para el gráfico de líneas
            asistencia_diaria = datos_filtrados.groupby(datos_filtrados['fecha'].dt.date).agg({
                'nombre': 'nunique',  # Empleados únicos por día
                'duracion_horas': 'sum'  # Total de horas trabajadas por día
            }).reset_index()
            asistencia_diaria.columns = ['Fecha', 'Empleados_Presentes', 'Total_Horas']
            
            # Crear tabs para diferentes vistas
            tab1, tab2 = st.tabs([" Horas Totales por Día", "📊 Análisis Semanal"])
            
            with tab1:
                st.subheader("� Volumen de Horas Trabajadas por Día")
                st.caption("*Total de horas laborales registradas cada día*")
                
                fig_horas = px.bar(
                    asistencia_diaria,
                    x='Fecha',
                    y='Total_Horas',
                    title="Horas Totales Trabajadas por Día",
                    color='Total_Horas',
                    color_continuous_scale='Blues'
                )
                fig_horas.update_layout(
                    xaxis_title="Fecha",
                    yaxis_title="Horas Trabajadas",
                    showlegend=False
                )
                fig_horas.update_traces(
                    hovertemplate="<b>%{x}</b><br>Horas: %{y:.1f}h<extra></extra>"
                )
                st.plotly_chart(fig_horas, use_container_width=True)
            
            with tab2:
                st.subheader("📊 Análisis por Día de la Semana")
                st.caption("*Patrones de asistencia según el día de la semana*")
                
                # Análisis por día de la semana
                asistencia_diaria['Dia_Semana'] = pd.to_datetime(asistencia_diaria['Fecha']).dt.day_name()
                dias_orden = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                nombres_dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
                
                resumen_semanal = asistencia_diaria.groupby('Dia_Semana').agg({
                    'Empleados_Presentes': ['mean', 'max', 'min'],
                    'Total_Horas': 'mean'
                }).round(1)
                
                # Reordenar por días de la semana
                resumen_semanal = resumen_semanal.reindex(dias_orden)
                resumen_semanal.index = nombres_dias
                
                # Gráfico de barras agrupadas
                fig_semanal = go.Figure()
                
                fig_semanal.add_trace(go.Bar(
                    name='Promedio Empleados',
                    x=nombres_dias,
                    y=resumen_semanal[('Empleados_Presentes', 'mean')],
                    marker_color='lightblue',
                    hovertemplate="<b>%{x}</b><br>Promedio: %{y:.1f} empleados<extra></extra>"
                ))
                
                fig_semanal.update_layout(
                    title="Asistencia Promedio por Día de la Semana",
                    xaxis_title="Día de la Semana",
                    yaxis_title="Número de Empleados",
                    showlegend=False
                )
                
                st.plotly_chart(fig_semanal, use_container_width=True)
                
                # Insights
                mejor_dia = resumen_semanal[('Empleados_Presentes', 'mean')].idxmax()
                peor_dia = resumen_semanal[('Empleados_Presentes', 'mean')].idxmin()
                
                st.info(f"💡 **Insights**: {mejor_dia} es el día con mayor asistencia promedio, mientras que {peor_dia} tiene la menor asistencia.")

        # Gráfico adicional 3: Promedio de horas trabajadas por área
        if 'duracion_horas' in datos_filtrados.columns and 'area' in datos_filtrados.columns and len(datos_filtrados) > 0:
            area_prom = datos_filtrados.groupby('area')['duracion_horas'].mean()
            st.subheader("🏗️ Productividad por Área")
            st.caption("*Promedio de horas trabajadas por jornada en cada área*")
            st.bar_chart(area_prom)
        
        # Métricas adicionales
        if len(datos_filtrados) > 0:
            st.subheader("📈 Métricas Adicionales")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if 'duracion_horas' in datos_filtrados.columns:
                    total_horas = datos_filtrados['duracion_horas'].sum()
                    st.metric("Total Horas Trabajadas", f"{total_horas:.1f}")
            
            with col2:
                personas_unicas = datos_filtrados['nombre'].nunique()
                st.metric("Personas Registradas", personas_unicas)
            
            with col3:
                areas_unicas = datos_filtrados['area'].nunique()
                st.metric("Áreas Activas", areas_unicas)
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")