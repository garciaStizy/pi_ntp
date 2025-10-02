import streamlit as st
import pandas as pd
import requests 


def cargar_datos_api():
    # Realizar petición GET a la API
    response = requests.get('https://68de838bd7b591b4b78fce39.mockapi.io/Horarios')

    # Verificar que la petición fue exitosa
    if response.status_code == 200:
        # Convertir la respuesta JSON a DataFrame
        data = response.json()
        df = pd.DataFrame(data)

        return df
    else:
        print(f"Error en la petición: {response.status_code}") 

    
def mostrar_horarios():
    st.sidebar.info("Visualiza los registros de horarios cargados en el sistema.")
    try:
        datos = cargar_datos_api()
        st.title("Registro de Horarios ⏰")

        # Filtro por nombre
        nombres = datos['nombre'].unique()
        nombre_sel = st.sidebar.selectbox("Filtrar por persona", options=['Todos'] + list(nombres))

        # Filtro múltiple por área
        areas = datos['area'].unique()
        areas_sel = st.sidebar.multiselect("Filtrar por área(s)", options=areas, default=[])

        # Filtro múltiple por rol
        roles = datos['rol'].unique()
        roles_sel = st.sidebar.multiselect("Filtrar por rol(es)", options=roles, default=[])

        # Filtro por rango de fechas
        fechas = pd.to_datetime(datos['fecha'])
        fecha_min = fechas.min()
        fecha_max = fechas.max()
        fecha_inicio, fecha_fin = st.sidebar.date_input(
            "Filtrar por rango de fechas",
            value=(fecha_min, fecha_max),
            min_value=fecha_min,
            max_value=fecha_max
        )

        # Filtro por hora de entrada (solo hora, no minutos)
        horas_entrada = datos['hora_entrada'].str[:2].astype(int)
        hora_min = horas_entrada.min()
        hora_max = horas_entrada.max()
        hora_entrada_rango = st.sidebar.slider(
            "Filtrar por hora de entrada",
            min_value=hora_min, max_value=hora_max,
            value=(hora_min, hora_max)
        )

        # Aplicar filtros
        datos_filtrados = datos.copy()
        if nombre_sel != 'Todos':
            datos_filtrados = datos_filtrados[datos_filtrados['nombre'] == nombre_sel]
        if areas_sel:
            datos_filtrados = datos_filtrados[datos_filtrados['area'].isin(areas_sel)]
        if roles_sel:
            datos_filtrados = datos_filtrados[datos_filtrados['rol'].isin(roles_sel)]
        datos_filtrados = datos_filtrados[
            (pd.to_datetime(datos_filtrados['fecha']) >= pd.to_datetime(fecha_inicio)) &
            (pd.to_datetime(datos_filtrados['fecha']) <= pd.to_datetime(fecha_fin))
        ]
        datos_filtrados = datos_filtrados[
            datos_filtrados['hora_entrada'].str[:2].astype(int).between(hora_entrada_rango[0], hora_entrada_rango[1])
        ]

        # Filtro: mostrar solo la persona con más horas trabajadas
        filtro_max_horas = st.sidebar.checkbox("Mostrar solo la persona con más horas trabajadas", value=False)
        if filtro_max_horas and 'hora_entrada' in datos_filtrados.columns and 'hora_salida' in datos_filtrados.columns and 'nombre' in datos_filtrados.columns:
            entrada = pd.to_datetime(datos_filtrados['fecha'] + ' ' + datos_filtrados['hora_entrada'])
            salida = pd.to_datetime(datos_filtrados['fecha'] + ' ' + datos_filtrados['hora_salida'])
            duracion = (salida - entrada).dt.total_seconds() / 3600
            duracion_df = pd.DataFrame({'nombre': datos_filtrados['nombre'], 'Duración': duracion})
            suma_horas = duracion_df.groupby('nombre').sum()
            persona_max = suma_horas['Duración'].idxmax()
            datos_filtrados = datos_filtrados[datos_filtrados['nombre'] == persona_max]

        st.subheader("Registros filtrados")
        st.dataframe(datos_filtrados.head(50))

        # Estadísticas generales
        st.subheader("Estadísticas generales")
        st.write(f"Total de registros: {len(datos_filtrados)}")
        # Gráfico 1: Promedio de horas trabajadas por persona
        if 'hora_entrada' in datos_filtrados.columns and 'hora_salida' in datos_filtrados.columns and 'nombre' in datos_filtrados.columns:
            try:
                entrada = pd.to_datetime(datos_filtrados['fecha'] + ' ' + datos_filtrados['hora_entrada'])
                salida = pd.to_datetime(datos_filtrados['fecha'] + ' ' + datos_filtrados['hora_salida'])
                duracion = (salida - entrada).dt.total_seconds() / 3600
                st.write(f"Promedio de horas trabajadas: {duracion.mean():.2f} horas")
                duracion_df = pd.DataFrame({'Nombre': datos_filtrados['nombre'], 'Duración': duracion})
                duracion_prom = duracion_df.groupby('Nombre').mean()
                st.subheader("Promedio de horas trabajadas por persona")
                st.bar_chart(duracion_prom)
            except Exception as e:
                st.warning(f"No se pudo calcular la duración: {e}")

        # Gráfico 2: Registros por área
        if 'area' in datos_filtrados.columns:
            area_df = datos_filtrados['area'].value_counts().rename_axis('Área').reset_index(name='Cantidad')
            area_df.set_index('Área', inplace=True)
            st.subheader("Cantidad de registros por área")
            st.bar_chart(area_df)

        # Gráfico 3: Registros por día (gráfico de barras)
        if 'fecha' in datos_filtrados.columns:
            conteo_dias = datos_filtrados['fecha'].value_counts().sort_index()
            conteo_dias_df = conteo_dias.rename_axis('Fecha').reset_index(name='Cantidad')
            conteo_dias_df.set_index('Fecha', inplace=True)
            st.subheader("Cantidad de registros por día")
            st.bar_chart(conteo_dias_df)

        # Gráfico adicional 3: Promedio de horas trabajadas por área
        if 'hora_entrada' in datos_filtrados.columns and 'hora_salida' in datos_filtrados.columns and 'area' in datos_filtrados.columns:
            try:
                entrada = pd.to_datetime(datos_filtrados['fecha'] + ' ' + datos_filtrados['hora_entrada'])
                salida = pd.to_datetime(datos_filtrados['fecha'] + ' ' + datos_filtrados['hora_salida'])
                duracion = (salida - entrada).dt.total_seconds() / 3600
                area_df = pd.DataFrame({'Área': datos_filtrados['area'], 'Duración': duracion})
                area_prom = area_df.groupby('Área').mean()
                st.subheader("Promedio de horas trabajadas por área")
                st.bar_chart(area_prom)
            except Exception as e:
                st.warning(f"No se pudo calcular el promedio de horas por área: {e}")

        # Gráfico adicional 4: Top 5 días con más registros
        if 'fecha' in datos_filtrados.columns:
            top_dias = datos_filtrados['fecha'].value_counts().nlargest(5).sort_index()
            top_dias_df = top_dias.rename_axis('Fecha').reset_index(name='Cantidad')
            top_dias_df.set_index('Fecha', inplace=True)
            st.subheader("Top 5 días con más registros")
            st.bar_chart(top_dias_df)

        # Gráfico adicional 1: Distribución de horas de entrada (histograma)
        if 'hora_entrada' in datos_filtrados.columns:
            import matplotlib.pyplot as plt
            horas = datos_filtrados['hora_entrada'].str[:2].astype(int)
            st.subheader("Distribución de horas de entrada (Histograma)")
            fig, ax = plt.subplots()
            ax.hist(horas, bins=range(horas.min(), horas.max()+2), edgecolor='black', align='left')
            ax.set_xlabel('Hora de entrada')
            ax.set_ylabel('Cantidad de registros')
            ax.set_xticks(range(horas.min(), horas.max()+1))
            st.pyplot(fig)
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")