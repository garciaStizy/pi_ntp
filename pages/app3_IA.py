
import streamlit as st

def mostrar_ia():
	st.title("IA - Consulta a API de Inteligencia Artificial 🤖")
	st.write("Esta sección permite interactuar con una API de IA. Ingresa tu consulta y obtén una respuesta.")

	consulta = st.text_area("Escribe tu consulta para la IA:")
	if st.button("Enviar consulta"):
		# Aquí se llamaría a la API de IA (simulado)
		st.info("(Simulación) Respuesta de la IA para: " + consulta)
	else:
		st.caption("La respuesta aparecerá aquí luego de enviar la consulta.")
