import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Quiniela Familiar 2026")

# ESTILO CSS PARA EL FORMATO OSCURO
st.markdown("""
    <style>
        .stApp { background-color: #0e1117; }
        .metric-card {
            background-color: #1c1f26;
            border: 1px solid #FFD700;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            color: #FFD700;
        }
        .metric-title { font-size: 14px; color: #aaa; margin-bottom: 5px; }
        .metric-value { font-size: 30px; font-weight: bold; }
        h1, h2 { color: #FFD700; }
    </style>
""", unsafe_allow_html=True)

archivo = 'Copa del Mundo-2026 trabajo.xlsx'

try:
    df = pd.read_excel(archivo, sheet_name='FIFA 2026', header=None, dtype=str)
    nombres = df.iloc[1, 9:].tolist()
    puntos = df.iloc[2, 9:].tolist()
    
    datos = []
    for n, p in zip(nombres, puntos):
        nombre_limpio = str(n).strip()
        punto_limpio = int(p) if str(p).isdigit() else 0
        if nombre_limpio and nombre_limpio != 'nan':
            datos.append({'Participante': nombre_limpio, 'Puntos': punto_limpio})
            
    df_ranking = pd.DataFrame(datos).sort_values(by='Puntos', ascending=False).reset_index(drop=True)
    df_ranking.index += 1 # Para que el ranking empiece en 1

    # TÍTULO
    st.title("🏆 QUINIELA FAMILIAR - WORLD CUP 2026")
    
    # TARJETAS DE ESTADO (Métricas)
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"<div class='metric-card'><div class='metric-title'>👑 Líder de la Quiniela</div><div class='metric-value'>{df_ranking.iloc[0]['Participante']}</div></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='metric-card'><div class='metric-title'>📈 Puntaje Máximo</div><div class='metric-value'>{df_ranking.iloc[0]['Puntos']} pts</div></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='metric-card'><div class='metric-title'>👥 Participantes Activos</div><div class='metric-value'>{len(df_ranking)}</div></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # TABLA Y GRÁFICA
    col_tab, col_graf = st.columns([1, 2])
    
    with col_tab:
        st.subheader("📋 Tabla de Posiciones")
        st.table(df_ranking.rename(columns={'Puntos': 'Aciertos Totales'}))
        
    with col_graf:
        st.subheader("📊 Rendimiento General")
        fig = px.bar(df_ranking, x='Participante', y='Puntos', color='Puntos',
                     color_continuous_scale=['#4d3d00', '#FFD700'])
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                          font_color="white", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error("Error al cargar datos. Asegúrate de que el archivo esté en la ruta correcta.")