import streamlit as st 
import pandas as pd

def mostrar_exploracion_datos():
    st.title("Exploración de Datos 📊")
    st.write("Aquí puedes explorar los datos disponibles.")
    # Ejemplo: mostrar un archivo CSV si existe
    try:
        datos = pd.read_csv('datos_exploracion.csv')
        st.dataframe(datos)
    except FileNotFoundError:
        st.warning("No se encontró el archivo 'datos_exploracion.csv'.")