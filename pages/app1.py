import streamlit as st
import pandas as pd

def mostrar_horarios():
    st.sidebar.info("Visualiza los registros de horarios cargados en el sistema.")
    try:
        datos = pd.read_csv('registros_horarios_reales.csv')
        st.title("Registro de Horarios ⏰")

        # Filtro por nombre
        nombres = datos['nombre'].unique()
        nombre_sel = st.sidebar.selectbox("Filtrar por persona", options=['Todos'] + list(nombres))

        # Filtro múltiple por área
        areas = datos['area'].unique()
        areas_sel = st.sidebar.multiselect("Filtrar por área(s)", options=areas, default=list(areas))

        # Filtro múltiple por rol
        roles = datos['rol'].unique()
        roles_sel = st.sidebar.multiselect("Filtrar por rol(es)", options=roles, default=list(roles))

        # Filtro por ID de usuario
        ids = datos['id_usuario'].unique()
        id_sel = st.sidebar.selectbox("Filtrar por ID de usuario", options=['Todos'] + list(map(str, ids)))

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
        if id_sel != 'Todos':
            datos_filtrados = datos_filtrados[datos_filtrados['id_usuario'] == int(id_sel)]
        datos_filtrados = datos_filtrados[
            (pd.to_datetime(datos_filtrados['fecha']) >= pd.to_datetime(fecha_inicio)) &
            (pd.to_datetime(datos_filtrados['fecha']) <= pd.to_datetime(fecha_fin))
        ]
        datos_filtrados = datos_filtrados[
            datos_filtrados['hora_entrada'].str[:2].astype(int).between(hora_entrada_rango[0], hora_entrada_rango[1])
        ]

        st.subheader("Registros filtrados")
        st.dataframe(datos_filtrados)

        # Estadísticas generales
        st.subheader("Estadísticas generales")
        st.write(f"Total de registros: {len(datos_filtrados)}")
        if 'hora_entrada' in datos_filtrados.columns and 'hora_salida' in datos_filtrados.columns:
            try:
                entrada = pd.to_datetime(datos_filtrados['fecha'] + ' ' + datos_filtrados['hora_entrada'])
                salida = pd.to_datetime(datos_filtrados['fecha'] + ' ' + datos_filtrados['hora_salida'])
                duracion = (salida - entrada).dt.total_seconds() / 3600
                st.write(f"Promedio de horas trabajadas: {duracion.mean():.2f} horas")
                # Crear un DataFrame para graficar la duración por persona (si existe la columna nombre)
                if 'nombre' in datos_filtrados.columns:
                    duracion_df = pd.DataFrame({'Nombre': datos_filtrados['nombre'], 'Duración': duracion})
                    duracion_df = duracion_df.groupby('Nombre').mean()
                    st.bar_chart(duracion_df)
                else:
                    duracion_df = pd.DataFrame({'Duración': duracion})
                    st.bar_chart(duracion_df)
            except Exception as e:
                st.warning(f"No se pudo calcular la duración: {e}")

        # Conteo por área
        if 'area' in datos_filtrados.columns:
            st.subheader("Registros por área")
            area_df = datos_filtrados['area'].value_counts().rename_axis('Área').reset_index(name='Cantidad')
            area_df.set_index('Área', inplace=True)
            st.bar_chart(area_df)

        # Conteo por rol
        if 'rol' in datos_filtrados.columns:
            st.subheader("Registros por rol")
            rol_df = datos_filtrados['rol'].value_counts().rename_axis('Rol').reset_index(name='Cantidad')
            rol_df.set_index('Rol', inplace=True)
            st.bar_chart(rol_df)

        # Conteo por fecha
        if 'fecha' in datos_filtrados.columns:
            conteo_dias = datos_filtrados['fecha'].value_counts().sort_index()
            conteo_dias_df = conteo_dias.rename_axis('Fecha').reset_index(name='Cantidad')
            conteo_dias_df.set_index('Fecha', inplace=True)
            st.subheader("Registros por día")
            st.line_chart(conteo_dias_df)
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")