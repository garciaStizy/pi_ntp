import streamlit as st
import pandas as pd

def mostrar_horarios():
    df = pd.read_csv("registro_horarios_excel.csv")
    st.title("Registro de Horarios ⏰")
    st.dataframe(df)
