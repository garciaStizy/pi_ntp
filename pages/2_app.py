## Aplicación 2 para un registro de un api
import streamlit as st
import pandas as pd

def mostrar_aeropuertos():
    datos = pd.read_csv('WL_B_Aeropuertos.csv')
    st.title("Registro de Aeropuertos ✈")
    st.dataframe(datos)