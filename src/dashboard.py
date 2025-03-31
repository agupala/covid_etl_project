"""Dashboard para visualizar datos de COVID-19 utilizando Streamlit y Plotly."""
import logging
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(layout="wide", page_title="COVID-19 Dashboard", page_icon="🦠")

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(module)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Cargar datos
@st.cache_data
def load_data():
    logging.info("Loading processed data...")
    df = pd.read_csv(".data/covid_data.csv", parse_dates=["date"])
    logging.info("Data loaded successfully. Shape: %s", df.shape)
    return df

df = load_data()

# Configuración de la página
st.title("🦠 COVID-19 Dashboard")
st.markdown("Análisis de casos, recuperaciones y muertes por COVID-19")

# Sidebar - Filtros
st.sidebar.header("Filtros")
selected_year = st.sidebar.selectbox(
    "Seleccionar año:",
    sorted(df["date"].dt.year.unique()),
    index=len(sorted(df["date"].dt.year.unique()))-1  # Último año por defecto
)

# Filtrar países con más casos para mejor visualización
top_countries = st.sidebar.slider(
    "Mostrar top N países:",
    min_value=5,
    max_value=30,
    value=15
)

# Opción para mostrar datos absolutos o per cápita
show_per_capita = st.sidebar.checkbox("Mostrar datos per cápita (por millón)")

# Filtrar datos por año
df_filtered = df[df["date"].dt.year == selected_year].copy()

# Calcular casos recuperados estimados
df_filtered["estimated_recovered"] = df_filtered["total_cases"] - df_filtered["total_deaths"]
df_filtered["active_cases"] = df_filtered["total_cases"] - df_filtered["estimated_recovered"] - df_filtered["total_deaths"]

# Agrupar datos por país y seleccionar top países
if show_per_capita:
    agg_data = df_filtered.groupby("location")[[
        "total_cases_per_million",
        "total_deaths_per_million"
    ]].max().reset_index()
    agg_data["estimated_recovered_per_million"] = agg_data["total_cases_per_million"] - agg_data["total_deaths_per_million"]
    agg_data["active_cases_per_million"] = agg_data["total_cases_per_million"] - agg_data["estimated_recovered_per_million"] - agg_data["total_deaths_per_million"]

    # Ordenar y seleccionar top países
    agg_data = agg_data.sort_values("total_cases_per_million", ascending=False).head(top_countries)
else:
    agg_data = df_filtered.groupby("location")[[
        "total_cases",
        "total_deaths",
        "estimated_recovered",
        "active_cases"
    ]].max().reset_index()

    # Ordenar y seleccionar top países
    agg_data = agg_data.sort_values("total_cases", ascending=False).head(top_countries)

# Gráfico 1: Casos, recuperados y muertes
st.markdown(f"## 📊 Situación COVID-19 en {selected_year}")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Casos totales por país")
    if show_per_capita:
        fig1 = px.bar(
            agg_data,
            x="location",
            y=["total_cases_per_million", "estimated_recovered_per_million", "total_deaths_per_million"],
            labels={"value": "Número de personas por millón", "location": "País", "variable": "Métrica"},
            title=f"Casos COVID-19 por millón de habitantes ({selected_year})",
            barmode="group",
            color_discrete_sequence=["#636EFA", "#00CC96", "#EF553B"]
        )
    else:
        fig1 = px.bar(
            agg_data,
            x="location",
            y=["total_cases", "estimated_recovered", "total_deaths"],
            labels={"value": "Número de personas", "location": "País", "variable": "Métrica"},
            title=f"Casos COVID-19 totales ({selected_year})",
            barmode="group",
            color_discrete_sequence=["#636EFA", "#00CC96", "#EF553B"]
        )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("### Proporción de casos activos, recuperados y fallecidos")
    if show_per_capita:
        fig2 = px.sunburst(
            agg_data,
            path=["location"],
            values="total_cases_per_million",
            color="total_deaths_per_million",
            hover_data=["estimated_recovered_per_million", "active_cases_per_million"],
            title=f"Distribución de casos por país ({selected_year})",
            color_continuous_scale="Reds"
        )
    else:
        fig2 = px.sunburst(
            agg_data,
            path=["location"],
            values="total_cases",
            color="total_deaths",
            hover_data=["estimated_recovered", "active_cases"],
            title=f"Distribución de casos por país ({selected_year})",
            color_continuous_scale="Reds"
        )
    st.plotly_chart(fig2, use_container_width=True)

# Gráfico 2: Evolución temporal
st.markdown("## 📈 Evolución temporal")

selected_countries = st.multiselect(
    "Seleccionar países para comparar:",
    options=agg_data["location"].unique(),
    default=agg_data["location"].head(3).tolist()
)

if selected_countries:
    df_countries = df_filtered[df_filtered["location"].isin(selected_countries)]

    fig3 = make_subplots(specs=[[{"secondary_y": True}]])

    for country in selected_countries:
        country_data = df_countries[df_countries["location"] == country]

        if show_per_capita:
            fig3.add_trace(
                go.Scatter(
                    x=country_data["date"],
                    y=country_data["new_cases_smoothed_per_million"],
                    name=f"{country} - Nuevos casos/millón",
                    line=dict(width=2)
                ),
                secondary_y=False
            )

            fig3.add_trace(
                go.Scatter(
                    x=country_data["date"],
                    y=country_data["new_deaths_smoothed_per_million"],
                    name=f"{country} - Nuevas muertes/millón",
                    line=dict(width=2, dash="dot")
                ),
                secondary_y=True
            )
        else:
            fig3.add_trace(
                go.Scatter(
                    x=country_data["date"],
                    y=country_data["new_cases_smoothed"],
                    name=f"{country} - Nuevos casos",
                    line=dict(width=2)
                ),
                secondary_y=False
            )

            fig3.add_trace(
                go.Scatter(
                    x=country_data["date"],
                    y=country_data["new_deaths_smoothed"],
                    name=f"{country} - Nuevas muertes",
                    line=dict(width=2, dash="dot")
                ),
                secondary_y=True
            )

    fig3.update_layout(
        title=f"Evolución diaria de casos y muertes en {selected_year}",
        xaxis_title="Fecha",
        hovermode="x unified"
    )

    if show_per_capita:
        fig3.update_yaxes(title_text="Nuevos casos por millón", secondary_y=False)
        fig3.update_yaxes(title_text="Nuevas muertes por millón", secondary_y=True)
    else:
        fig3.update_yaxes(title_text="Nuevos casos", secondary_y=False)
        fig3.update_yaxes(title_text="Nuevas muertes", secondary_y=True)

    st.plotly_chart(fig3, use_container_width=True)

# Métricas clave
st.markdown("## 🔍 Métricas clave")

col1, col2, col3, col4 = st.columns(4)

total_cases = df_filtered["total_cases"].max()
total_deaths = df_filtered["total_deaths"].max()
recovery_rate = ((df_filtered["estimated_recovered"].max() / total_cases) * 100) if total_cases > 0 else 0
mortality_rate = ((total_deaths / total_cases) * 100) if total_cases > 0 else 0

col1.metric("Casos totales", f"{total_cases:,.0f}")
col2.metric("Muertes totales", f"{total_deaths:,.0f}")
col3.metric("Tasa de recuperación", f"{recovery_rate:.2f}%")
col4.metric("Tasa de mortalidad", f"{mortality_rate:.2f}%")

# Mapa mundial
st.markdown("## 🌍 Distribución geográfica")

if show_per_capita:
    map_df = df_filtered.groupby(["location", "iso_code"])["total_cases_per_million"].max().reset_index()
    fig_map = px.choropleth(
        map_df,
        locations="iso_code",
        color="total_cases_per_million",
        hover_name="location",
        color_continuous_scale="OrRd",
        title=f"Casos totales por millón de habitantes ({selected_year})",
        labels={"total_cases_per_million": "Casos por millón"}
    )
else:
    map_df = df_filtered.groupby(["location", "iso_code"])["total_cases"].max().reset_index()
    fig_map = px.choropleth(
        map_df,
        locations="iso_code",
        color="total_cases",
        hover_name="location",
        color_continuous_scale="OrRd",
        title=f"Casos totales ({selected_year})",
        labels={"total_cases": "Casos totales"}
    )

st.plotly_chart(fig_map, use_container_width=True)
logging.info("Dashboard actualizado exitosamente.")
