import pandas as pd
import random
from datetime import datetime, timedelta

# Número de registros
n = 10000

# Lista de nombres ficticios
nombres = ["Samuel Bernal", "Cristian Sierra", "Harrison Rengifo", "Sebastian Garcia", 
           "Santiago Puerta", "Carlos Perez", "Laura Gomez", "Ana Torres", 
           "David Morales", "Maria Sanchez"]

# Generar datos
data = []
start_date = datetime(2025, 1, 1)

for i in range(n):
    trabajador = random.choice(nombres)
    cedula = random.randint(10000000, 99999999)
    fecha = start_date + timedelta(days=random.randint(0, 240))
    
    entrada_oficial = datetime.combine(fecha.date(), datetime.strptime("07:30", "%H:%M").time())
    entrada_real = entrada_oficial + timedelta(minutes=random.randint(0, 60))
    salida_real = entrada_real + timedelta(hours=8, minutes=random.randint(-30, 30))
    
    tardanza = max(0, int((entrada_real - entrada_oficial).total_seconds() // 60))
    
    data.append([
        trabajador,
        cedula,
        fecha.strftime("%Y-%m-%d"),
        entrada_real.strftime("%H:%M"),
        salida_real.strftime("%H:%M"),
        tardanza,
        "Tarde" if tardanza > 0 else "-"
    ])

# Crear DataFrame
df = pd.DataFrame(data, columns=["Trabajador", "Cédula", "Fecha", "Entrada", "Salida", "Minutos Tarde", "Observación"])

# Guardar con separador ";"
df.to_csv("registro_horarios_excel.csv", index=False, sep=";")
