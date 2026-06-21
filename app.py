import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de página amplia
st.set_page_config(layout="wide", page_title="World Cup 2026 - Analytics")

# ESTILO CSS
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
        h1, h2, h3 { color: #FFD700 !class; }
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
    df_ranking.index += 1
    
    # --- LÓGICA DE RESALTADO (TOP 20) ---
    df_ranking['Pos'] = df_ranking.index
    df_ranking['Estado'] = df_ranking['Pos'].apply(lambda x: '✅ TOP 20 - PASA' if x <= 20 else '❌ ELIMINADO')

    # TÍTULO
    st.title("🏢 World Cup 2026: Leaderboard & Analytics")
    st.subheader("🎯 Fase de Clasificación: Los mejores 20 avanzan de ronda")
    st.markdown("---")
    
    # TARJETAS DEL PODIO
    c1, c2, c3 = st.columns(3)
    for i, col in enumerate([c1, c2, c3]):
        emoji = ["🥇", "🥈", "🥉"][i]
        color = ["#FFD700", "#C0C0C0", "#CD7F32"][i]
        col.markdown(f"""
            <div class='metric-card' style='border-color: {color};'>
                <div class='metric-title'>{emoji} {i+1}ER LUGAR</div>
                <div style='font-size: 24px; font-weight: bold; color: {color};'>{df_ranking.iloc[i]['Participante']}</div>
                <div style='color: #aaa;'>{df_ranking.iloc[i]['Puntos']} pts</div>
            </div>
        """, unsafe_allow_html=True)

    # TABLA Y GRÁFICA
    col_tab, col_graf = st.columns([1.2, 2])
    
    with col_tab:
        st.subheader("📋 Clasificación")
        # Estilizado de la tabla: Resaltamos visualmente el DataFrame
        st.dataframe(
            df_ranking[['Pos', 'Participante', 'Puntos', 'Estado']], 
            use_container_width=True, 
            hide_index=True
        )
        
    with col_graf:
        st.subheader("📊 Gráfico de Clasificación")
        # Gráfico con colores condicionales: Dorado para clasificados, Gris para eliminados
        fig = px.bar(
            df_ranking, 
            x='Participante', 
            y='Puntos', 
            color='Estado',
            color_discrete_map={'✅ TOP 20 - PASA': '#FFD700', '❌ ELIMINADO': '#444444'},
            category_orders={"Participante": df_ranking['Participante'].tolist()}
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)',
            font_color="white", 
            showlegend=True,
            legend_title_text=''
        )
        # Línea de corte visual en el gráfico
        if len(df_ranking) >= 20:
            corte = df_ranking.iloc[19]['Puntos']
            fig.add_hline(y=corte, line_dash="dot", line_color="white", annotation_text="Línea de Corte")

        st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
