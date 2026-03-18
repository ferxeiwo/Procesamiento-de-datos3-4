import pandas as pd
import random
from datetime import datetime, timedelta

# usar tu conexión
from conexiones import conectar


# ---------------- EXTRACCIÓN ----------------

def extraer_datos():
    try:
        engine = conectar()

        clientes = pd.read_sql("SELECT * FROM clientes", engine)
        ventas = pd.read_sql("SELECT * FROM ventas", engine)

        print("Datos extraídos correctamente")
        return clientes, ventas

    except Exception as e:
        print("Error al extraer datos:", e)
        return pd.DataFrame(), pd.DataFrame()


# ---------------- GENERAR DATOS (si no existen) ----------------

def generar_clientes():
    data = []
    ciudades = ["Culiacan", "Mazatlan", "Los Mochis"]

    for i in range(1, 501):
        data.append({
            "id": i,
            "nombre": f"Cliente_{i}",
            "ciudad": random.choice(ciudades)
        })

    return pd.DataFrame(data)


def generar_ventas():
    data = []

    for i in range(3000):
        data.append({
            "id_cliente": random.randint(1, 500),
            "monto": random.randint(100, 5000),
            "fecha": datetime.now() - timedelta(days=random.randint(1, 365))
        })

    return pd.DataFrame(data)


# ---------------- TRANSFORMACIÓN ----------------

def transformar(clientes, ventas):

    # eliminar duplicados
    clientes = clientes.drop_duplicates()
    ventas = ventas.drop_duplicates()

    # eliminar nulos
    clientes = clientes.dropna()
    ventas = ventas.dropna()

    # convertir fecha
    ventas["fecha"] = pd.to_datetime(ventas["fecha"])

    # unir tablas
    df = pd.merge(clientes, ventas, left_on="id", right_on="id_cliente")

    # total gastado por cliente
    total = df.groupby("id")["monto"].sum().reset_index()
    total.rename(columns={"monto": "total_gastado"}, inplace=True)

    # unir total
    df_final = pd.merge(df, total, on="id")

    return df_final


# ---------------- CARGA ----------------

def cargar_csv(df):
    df.to_csv("resultado_final.csv", index=False)
    print("CSV generado correctamente")


# ---------------- MAIN ----------------

if __name__ == "__main__":

    clientes, ventas = extraer_datos()

    # si no hay datos, los generamos
    if clientes.empty:
        print("Generando clientes...")
        clientes = generar_clientes()

    if ventas.empty:
        print("Generando ventas...")
        ventas = generar_ventas()

    # transformación
    df_final = transformar(clientes, ventas)

    # carga
    cargar_csv(df_final)