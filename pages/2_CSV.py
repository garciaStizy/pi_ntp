## Aplicación 2 para un registro de un api
import streamlit as st
import pandas as pd
datos = pd.read_csv('pages\WL_B_Aeropuertos.csv')
st.title("Registro de Aeropuertos ✈")
st.dataframe(datos)   