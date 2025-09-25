## Aplicación 2 para un registro de un api
import streamlit as st
import pandas as pd
def mostrar_RegistroEducativos():
    st.sidebar.info("Consulta los registros de centros educativos disponibles.")
    datos = pd.read_csv('WL_T_Centros_Educativos.csv')
    st.title("Registros educativos ✈")

    # Filtros
    municipios = datos['MUNICIPIO'].dropna().unique()
    municipio_sel = st.sidebar.multiselect("Filtrar por municipio", municipios, default=list(municipios))
    categoria = datos['CATEGORIA'].dropna().unique()
    categoria_sel = st.sidebar.multiselect("Filtrar por categoría", categoria, default=list(categoria))
    estado = datos['Estado_InfraestructuraE'].dropna().unique()
    estado_sel = st.sidebar.multiselect("Filtrar por estado infraestructura", estado, default=list(estado))

    datos_filtrados = datos[
        datos['MUNICIPIO'].isin(municipio_sel) &
        datos['CATEGORIA'].isin(categoria_sel) &
        datos['Estado_InfraestructuraE'].isin(estado_sel)
    ]

    st.subheader(f"Registros filtrados: {len(datos_filtrados)}")
    st.dataframe(datos_filtrados)

    # Gráficos importantes
    st.subheader("Distribución por municipio")
    st.bar_chart(datos_filtrados['MUNICIPIO'].value_counts())

    st.subheader("Distribución por estado de infraestructura")
    st.bar_chart(datos_filtrados['Estado_InfraestructuraE'].value_counts())

    st.subheader("Distribución por categoría")
    st.bar_chart(datos_filtrados['CATEGORIA'].value_counts())