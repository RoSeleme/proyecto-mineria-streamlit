
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(page_title="Siniestros viales fatales (2017-2023)", layout="wide")

# ---------- Carga de datos ----------
@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/dataset_limpio.csv")
    return df

df = load_data()

# TÍTULO Y DESCRIPCIÓN GENERAL
st.title("Análisis Exploratorio de Siniestros Viales Fatales en Argentina (2017 - 2023)")
st.caption("Fuente: datos.gob.ar | Sistema de Alerta Temprana (SAT) | Unidad de análisis: víctimas fatales")
st.markdown("Dashboard interactivo para explorar patrones temporales, geográficos y por tipo de vehículo.")

#st.subheader("Vista general del dataset")
#st.dataframe(df.head())
#LO MUESTRO DESPUES DE LA CREACION DE FILTROS



# ------ Filtros (sidebar) por año y provincia ------
st.sidebar.header("Filtros")

anios = sorted(df["anio"].dropna().unique())
anio_sel = st.sidebar.multiselect("Año", options=anios, default=anios)

provincias = sorted(df["provincia_nombre"].dropna().unique())
prov_sel = st.sidebar.multiselect("Provincia", options=provincias, default=provincias)

# Aplicar filtros
df_f = df[df["anio"].isin(anio_sel) & df["provincia_nombre"].isin(prov_sel)].copy()

# para cuando el usuario borra todos los años o provincias.
if df_f.empty:
    st.warning("No hay datos con los filtros seleccionados. Ajuste Año/Provincia.")
    st.stop()


# Vista general del dataframe
st.subheader("Vista general del dataset")
st.dataframe(df_f.head())

st.divider()   # para dividir secciones


# -------------  KPIs (métricas claves) --------------
st.subheader("KPIs Claves")

col1, col2, col3, col4 = st.columns(4)

total_victimas = len(df_f)
total_siniestros = df_f["id_hecho"].nunique() if "id_hecho" in df_f.columns else None

df_geo = df_f.dropna(subset=["latitud", "longitud"])
pct_geo = (len(df_geo) / len(df_f) * 100) if len(df_f) else 0

# Edad - Rango etario más frecuente (moda) ya que la variable edad esta agrupada por rangos
rango_moda = df_f["victima_tr_edad"].astype(str).replace("nan", pd.NA).dropna()
rango_moda = rango_moda.mode().iloc[0] if len(rango_moda) else None

# Visualizacion
col1.metric("Total Víctimas (registros)", f"{total_victimas:,}".replace(",", "."))
col2.metric("Total Siniestros (id_hecho únicos)", f"{total_siniestros:,}".replace(",", ".") if total_siniestros is not None else "—")
col3.metric("Cobertura del mapa (% coordenadas )", f"{pct_geo:.1f}%")
col4.metric("Rango etario más frecuente", f"{rango_moda} años" if rango_moda else "—")

st.divider()


# ------------------  Serie temporal mensual + MM12 ------------------
st.subheader("Evolución mensual de víctimas (MM12)")

df_ts = df_f.copy()
df_ts["fecha_mes"] = pd.to_datetime(df_ts["anio"].astype(str) + "-" + df_ts["mes_num"].astype(str) + "-01",errors="coerce")

ts = (
    df_ts.dropna(subset=["fecha_mes"])
        .groupby("fecha_mes")
        .size()
        .rename("victimas")
        .to_frame()
        .sort_index()
)

ts["mm_12"] = ts["victimas"].rolling(12, min_periods=1).mean()

fig_ts = px.line(ts, y=["victimas", "mm_12"])
fig_ts.update_layout(legend_title_text="", xaxis_title="Mes", yaxis_title="Víctimas")
st.plotly_chart(fig_ts, use_container_width=True)

st.caption(
    "**Se observa un quiebre marcado en 2020**: la serie cae abruptamente y luego muestra recuperación gradual. "
    "Este patrón es consistente con cambios en la movilidad durante el período de pandemia, aunque no permite afirmar causalidad."
)


st.divider()


# ---------  Estacionalidad por mes (barras) ----------

st.subheader("Estacionalidad: Promedio de Víctimas fatales por mes")

ts_est = ts.copy()
ts_est["mes"] = ts_est.index.month

est = ts_est.groupby("mes")["victimas"].mean().reset_index()
est.columns = ["mes", "promedio_victimas"]

fig_est = px.bar(est, x="mes", y="promedio_victimas")
fig_est.update_layout(xaxis_title="Mes", yaxis_title="Promedio de víctimas")
st.plotly_chart(fig_est, use_container_width=True)

st.divider()


# ------------------  Top provincias ------------------
st.subheader("Top provincias por víctimas (según filtros)")

# Gráfico de barra vertical más sencillo
#top_prov = df_f["provincia_nombre"].value_counts().head(10).reset_index()
#top_prov.columns = ["provincia", "victimas"]
#fig_prov = px.bar(top_prov, x="provincia", y="victimas")
#fig_prov.update_layout(xaxis_title="Provincia", yaxis_title="Víctimas")
#st.plotly_chart(fig_prov, use_container_width=True)

#Gráfico de barra horizontal 
df_prov_top = (
    df_f["provincia_nombre"]
    .value_counts()
    .head(10)
    .reset_index()
)
df_prov_top.columns = ["Provincia", "Víctimas"]

fig_prov = px.bar(
    df_prov_top,
    x="Víctimas",
    y="Provincia",
    orientation="h",
    title="Top 10 provincias con mayor cantidad de víctimas",
    labels={"Víctimas": "Cantidad de víctimas", "Provincia": "Provincia"},
)

fig_prov.update_layout(
    yaxis={"categoryorder": "total ascending"},
    height=450,
    title_x=0.5
)

st.plotly_chart(fig_prov, use_container_width=True)


st.divider()


# ------------------  Vehículos (ampliado) ------------------
st.subheader("Víctimas Fatales según el tipo de vehículo ")

veh = df_f["victima_vehiculo_ampliado"].value_counts().head(12).reset_index()
veh.columns = ["vehiculo", "victimas"]
fig_veh = px.bar(veh, x="vehiculo", y="victimas")
fig_veh.update_layout(xaxis_title="Tipo de vehículo", yaxis_title="Víctimas")
st.plotly_chart(fig_veh, use_container_width=True)


st.divider()


# ------------------  Mapa (opcional) ------------------
st.subheader("Mapa Geográfico  (solo registros con coordenadas válidas)")

df_mapa = df_f.dropna(subset=["latitud", "longitud"]).copy()
df_mapa = df_mapa[
    df_mapa["latitud"].between(-56, -20) &
    df_mapa["longitud"].between(-75, -50)
].copy()

if len(df_mapa) == 0:
    st.info("No hay registros georreferenciados para los filtros seleccionados.")
else:
    df_map_plot = df_mapa.rename(columns={"latitud": "lat", "longitud": "lon"})   # st.map streamlit requiere 'lat' y 'lon'. Por eso se renombra las columnas
    st.map(df_map_plot[["lat", "lon"]])



