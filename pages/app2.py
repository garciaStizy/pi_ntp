## Aplicación 2 para un registro de un api
import streamlit as st
import pandas as pd
def mostrar_RegistroEducativos():

    datos = pd.read_csv('WL_T_Centros_Educativos.csv')
    st.title("Registros educativos ✈")
    st.dataframe(datos)