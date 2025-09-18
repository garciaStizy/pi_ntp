import streamlit as st
from 
st.sidebar.title("Menú")
opcion = st.sidebar.selectbox("Selecciona una opción", ["Horarios", "Aeropuertos"])

if opcion == "Horarios":
    mostrar_horarios()
elif opcion == "Aeropuertos":
    mostrar_aeropuertos()