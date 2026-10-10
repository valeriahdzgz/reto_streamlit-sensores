import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Reto Semanal - Monitoreo Industrial",
    layout="wide"
)

@st.cache_data
def cargar_datos():
    # Reemplazar por el nombre de su archivo descargado
    df = pd.read_csv("datos_sensores.csv")
    return df

df = cargar_datos()

st.title("Panel de Depuración y Visualización de Sensores")

# Filtrar solo columnas numéricas para evitar errores con cadenas/texto
df_num = df.select_dtypes(include=[np.number])

# Panel de Métricas (KPIs)
c1, c2, c3 = st.columns(3)
c1.metric("Total de Registros", len(df))

if not df_num.empty:
    # Toma la primera columna numérica para el promedio
    c2.metric(f"Promedio {df_num.columns[0]}", f"{df_num.iloc[:, 0].mean():.2f}")
    # Toma la segunda columna numérica para el máximo
    col_y = df_num.columns[1] if len(df_num.columns) > 1 else df_num.columns[0]
    c3.metric(f"Máximo {col_y}", f"{df_num[col_y].max():.2f}")
else:
    c2.metric("Promedio Variable X", "N/A")
    c3.metric("Máximo Variable Y", "N/A")

# Pestañas con visualizaciones interactivas
tab1, tab2 = st.tabs(["📈 Gráfico 2D/3D Plotly", "🔥 Matriz de Correlación"])

with tab1:
    st.subheader("Gráfico Interactivo de Dispersión")
    if len(df_num.columns) >= 2:
        col_x = df_num.columns[0]
        col_y = df_num.columns[1]
        col_color = df.columns[2] if len(df.columns) > 2 else None
        fig_scatter = px.scatter(df, x=col_x, y=col_y, color=col_color)
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.write("Se necesitan al menos dos columnas numéricas para este gráfico.")

with tab2:
    st.subheader("Mapa de Calor Seaborn")
    fig_sns, ax = plt.subplots()
    sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig_sns)