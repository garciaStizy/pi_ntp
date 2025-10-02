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
    municipio_df = datos_filtrados['MUNICIPIO'].value_counts().rename_axis('Municipio').reset_index(name='Cantidad')
    municipio_df.set_index('Municipio', inplace=True)
    st.bar_chart(municipio_df)

    st.subheader("Distribución por estado de infraestructura")
    estado_df = datos_filtrados['Estado_InfraestructuraE'].value_counts().rename_axis('Estado').reset_index(name='Cantidad')
    estado_df.set_index('Estado', inplace=True)
    st.bar_chart(estado_df)

    st.subheader("Distribución por categoría")
    categoria_df = datos_filtrados['CATEGORIA'].value_counts().rename_axis('Categoría').reset_index(name='Cantidad')
    categoria_df.set_index('Categoría', inplace=True)
    st.bar_chart(categoria_df)