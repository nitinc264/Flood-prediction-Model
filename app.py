# app.py — Streamlit Dashboard for RiskRadar
# Run with: streamlit run app.py
# Make sure api.py is running first: uvicorn api:app --reload --port 8000

import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import os

# ─── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RiskRadar — Flood Monitor",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_URL = "http://localhost:8000"

# ─── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .risk-high   { background: #fee2e2; border-left: 4px solid #ef4444;
                   padding: 12px 16px; border-radius: 6px; }
    .risk-medium { background: #fef3c7; border-left: 4px solid #f59e0b;
                   padding: 12px 16px; border-radius: 6px; }
    .risk-low    { background: #d1fae5; border-left: 4px solid #10b981;
                   padding: 12px 16px; border-radius: 6px; }
    .metric-box  { background: #f8fafc; border: 1px solid #e2e8f0;
                   padding: 16px; border-radius: 8px; text-align: center; }
</style>
""", unsafe_allow_html=True)

# ─── Header ──────────────────────────────────────────────────────────────────
st.title("🌊 RiskRadar — Flood Risk Prediction System")
st.markdown("*Powered by XGBoost · Built by Nitin Chauhan*")
st.divider()

# ─── API Health Check ────────────────────────────────────────────────────────
try:
    health = requests.get(f"{API_URL}/health", timeout=3).json()
    st.success(f"API connected ✓ | Model: {health.get('model')} | Features: {health.get('features')}")
except Exception:
    st.error("Cannot connect to API. Run: `uvicorn api:app --reload --port 8000` in your terminal first.")
    st.stop()

# ─── Sidebar — Input Parameters ──────────────────────────────────────────────
with st.sidebar:
    st.header("📊 Input Parameters")
    st.caption("Adjust hydrological and climate features")

    st.subheader("💧 Precipitation")
    annual_precipitation = st.slider("Annual Precipitation (mm)", 0, 3000, 1200, 50)
    wettest_month = st.slider("Wettest Month Precipitation (mm)", 0, 1000, 300, 10)
    precip_seasonality = st.slider("Precipitation Seasonality (%)", 0, 100, 50, 1)

    st.subheader("🏞️ Drainage & Terrain")
    drainage_density = st.slider("Drainage Density (km/km²)", 0.0, 10.0, 2.5, 0.1)
    drainage_texture = st.slider("Drainage Texture", 0.0, 50.0, 10.0, 0.5)
    basin_relief = st.slider("Basin Relief (m)", 0, 5000, 500, 50)
    ruggedness = st.slider("Ruggedness Number", 0.0, 5.0, 0.5, 0.1)
    infiltration = st.slider("Infiltration Number", 0.0, 20.0, 5.0, 0.5)
    curve_number = st.slider("Curve Number (AMC II)", 0.0, 100.0, 70.0, 1.0)

    st.subheader("🌡️ Climate & Land")
    temperature = st.slider("Annual Mean Temperature (°C)", -20, 40, 20, 1)
    temp_seasonality = st.slider("Temperature Seasonality", 0, 1500, 500, 10)
    climate_type = st.selectbox("Climate Type (encoded)", options=list(range(6)), index=2)
    landcover_type = st.selectbox("Landcover Type (encoded)", options=list(range(6)), index=1)
    soil_type = st.selectbox("Soil Type (encoded)", options=list(range(6)), index=3)

    predict_btn = st.button("🔍 Predict Flood Risk", type="primary", use_container_width=True)

# ─── Main Panel ──────────────────────────────────────────────────────────────
col_result, col_gauge = st.columns([1, 1])

if predict_btn:
    payload = {
        "annual_precipitation": annual_precipitation,
        "precipitation_of_wettest_month": wettest_month,
        "precipitation_seasonality": precip_seasonality,
        "drainage_density": drainage_density,
        "drainage_texture": drainage_texture,
        "basin_relief": basin_relief,
        "annual_mean_temperature": temperature,
        "temperature_seasonality": temp_seasonality,
        "curve_number_amcii": curve_number,
        "ruggedness_number": ruggedness,
        "infiltration_number": infiltration,
        "climate_type": climate_type,
        "landcover_type": landcover_type,
        "soil_type": soil_type
    }

    with st.spinner("Analyzing flood risk..."):
        try:
            response = requests.post(f"{API_URL}/predict", json=payload, timeout=10)
            result = response.json()

            risk_score = result["flood_risk_score"]
            risk_level = result["risk_level"]
            risk_pct = result["risk_percentage"]

            # ── Result box ───────────────────────────────────────────────────
            with col_result:
                st.subheader("Prediction Result")

                css_class = f"risk-{risk_level.lower()}"
                icon = "🚨" if risk_level == "HIGH" else "⚡" if risk_level == "MEDIUM" else "✅"
                st.markdown(
                    f'<div class="{css_class}">'
                    f'<h3>{icon} {risk_level} FLOOD RISK</h3>'
                    f'<p><b>Risk Score:</b> {risk_score:.4f}</p>'
                    f'<p><b>Probability:</b> {risk_pct}</p>'
                    f'<p>{result["message"]}</p>'
                    f'</div>',
                    unsafe_allow_html=True
                )

                st.markdown("")
                m1, m2, m3 = st.columns(3)
                m1.metric("Risk Score", f"{risk_score:.3f}")
                m2.metric("Risk Level", risk_level)
                m3.metric("Confidence", risk_pct)

            # ── Gauge chart ──────────────────────────────────────────────────
            with col_gauge:
                st.subheader("Risk Gauge")
                fig = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=risk_score * 100,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Flood Risk %", 'font': {'size': 18}},
                    delta={'reference': 40, 'increasing': {'color': "red"}},
                    gauge={
                        'axis': {'range': [0, 100], 'tickwidth': 1},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 40], 'color': '#d1fae5'},
                            {'range': [40, 70], 'color': '#fef3c7'},
                            {'range': [70, 100], 'color': '#fee2e2'}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 70
                        }
                    }
                ))
                fig.update_layout(height=300, margin=dict(t=40, b=20, l=20, r=20))
                st.plotly_chart(fig, use_container_width=True)

            # ── Input summary ────────────────────────────────────────────────
            st.divider()
            st.subheader("📋 Input Summary")
            summary_df = pd.DataFrame({
                "Parameter": [
                    "Annual Precipitation", "Wettest Month", "Seasonality",
                    "Drainage Density", "Basin Relief", "Temperature",
                    "Curve Number", "Ruggedness"
                ],
                "Value": [
                    f"{annual_precipitation} mm", f"{wettest_month} mm",
                    f"{precip_seasonality}%", f"{drainage_density} km/km²",
                    f"{basin_relief} m", f"{temperature}°C",
                    str(curve_number), str(ruggedness)
                ]
            })
            st.dataframe(summary_df, use_container_width=True, hide_index=True)

        except requests.exceptions.ConnectionError:
            st.error("Lost connection to API. Is the FastAPI server still running?")
        except Exception as e:
            st.error(f"Prediction error: {e}")

else:
    # Default state
    with col_result:
        st.info("👈 Set parameters in the sidebar and click **Predict Flood Risk** to get results.")
    with col_gauge:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=0,
            title={'text': "Flood Risk %"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "lightgray"},
                'steps': [
                    {'range': [0, 40], 'color': '#d1fae5'},
                    {'range': [40, 70], 'color': '#fef3c7'},
                    {'range': [70, 100], 'color': '#fee2e2'}
                ]
            }
        ))
        fig.update_layout(height=300, margin=dict(t=40, b=20, l=20, r=20))
        st.plotly_chart(fig, use_container_width=True)

# ─── High Risk Map (if CSV exists) ───────────────────────────────────────────
st.divider()
st.subheader("🗺️ High Risk Locations Map")

csv_path = "high_risk_locations.csv"
if os.path.exists(csv_path):
    risk_df = pd.read_csv(csv_path).dropna()
    if not risk_df.empty:
        fig_map = px.scatter_mapbox(
            risk_df,
            lat="latitude", lon="longitude",
            color="predicted_risk",
            size="predicted_risk",
            color_continuous_scale="RdYlGn_r",
            range_color=[0.7, 1.0],
            mapbox_style="carto-positron",
            zoom=2,
            title="High Risk Flood Locations (predicted_risk > 0.7)",
            labels={"predicted_risk": "Risk Score"}
        )
        fig_map.update_layout(height=500, margin=dict(t=40, b=0, l=0, r=0))
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.warning("high_risk_locations.csv is empty.")
else:
    st.info("Run the Colab notebook to generate `high_risk_locations.csv`, then place it in the same folder as app.py.")

st.caption("RiskRadar v1.0 · Built by Nitin Chauhan · XGBoost + FastAPI + Streamlit")