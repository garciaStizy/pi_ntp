import streamlit as st
import pandas as pd
from proyecto import mostrar_horarios
from aeropuertos import mostrar_aeropuertos  # <-- Importa la función


st.header("Panel Principal")


st.subheader("Sección Horarios")
mostrar_horarios()


st.subheader("Sección Aeropuertos")
mostrar_aeropuertos()  # <-- Muestra la segunda función
