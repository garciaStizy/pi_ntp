import streamlit as st
from proyecto import mostrar_horarios
from aeropuertos import mostrar_aeropuertos

st.header("Panel Principal")

# Selector en la barra lateral
opcion = st.sidebar.radio(
    "Selecciona la vista:",
    ("Horarios", "Aeropuertos")
)

if opcion == "Horarios":
    st.subheader("Sección Horarios")
    mostrar_horarios()
elif opcion == "Aeropuertos":
    st.subheader("Sección Aeropuertos")
    mostrar_aeropuertos()
