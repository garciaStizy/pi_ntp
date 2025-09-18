import streamlit as st
import pandas as pd

def mostrar_horarios():
    datos = pd.read_csv('registros_horarios_reales.csv')
    st.title("Registro de Horarios ⏰")
    st.dataframe(datos)