import streamlit as st

from pages.app1 import mostrar_horarios
from pages.app2 import mostrar_RegistroEducativos
from pages.app3_IA import mostrar_ia
from pages.app4_ExploracionDatos import mostrar_exploracion_datos

st.set_page_config(page_title="Panel Principal", layout="centered")

st.title("Panel Principal 📋")
st.write("Selecciona una aplicación para visualizar:")

opcion = st.sidebar.selectbox(
    "Aplicaciones disponibles",
    (
        "Inicio",
        "Registro de Horarios",
        "Centros educativos",
        "IA",
        "Exploración de Datos"
    )
)

if opcion == "Inicio":
    st.subheader("Bienvenido al panel principal.")
    st.write("Usa el menú lateral para navegar entre las aplicaciones.")
elif opcion == "Registro de Horarios":
    mostrar_horarios()
elif opcion == "Centros educativos":
    mostrar_RegistroEducativos()
elif opcion == "IA":
    mostrar_ia()
elif opcion == "Exploración de Datos":
    mostrar_exploracion_datos()

