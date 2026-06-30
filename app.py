import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de página
st.set_page_config(layout="wide", page_title="World Cup 2026 - Dieciseisavos")

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
        h1, h2, h3 { color: #FFD700 !important; }
    </style>
""", unsafe_allow_html=True)

archivo = 'Copa del Mundo-2026 trabajo.xlsx'
NOMBRE_PESTANA = 'DIECISEISAVOS'

@st.cache_data(ttl=30)
def cargar_datos():
    try:
        # Cargar la pestaña específica
        df = pd.read_excel(archivo, sheet_name=NOMBRE_PESTANA, header=None, dtype=str)
        
        # --- REFERENCIAS ---
        # Goles Reales: Celda H36 -> Fila índice 35, Columna índice 7 (H)
        try:
            goles_reales = int(float(df.iloc[35, 7]))
        except:
            goles_reales = 0

        # Participantes: Fila 2 (index 1), Columna J en adelante (index 9)
        nombres = df.iloc[1, 9:].tolist()
        # Puntos: Fila 3 (index 2)
        puntos = df.iloc[2, 9:].tolist()
        # Predicciones Goles: Fila 36 (index 35), Columna J en adelante (index 9)
        pred_goles = df.iloc[35, 9:].tolist()
        
        datos = []
        for i in range(len(nombres)):
            nombre_limpio = str(nombres[i]).strip()
            if nombre_limpio == 'nan' or not nombre_limpio:
                continue
                
            try:
                p = int(float(puntos[i]))
                g_p = int(float(pred_goles[i]))
            except:
                p, g_p = 0, 0
            
            # Cálculo de diferencia para desempate
            dif = abs(g_p - goles_reales)
            
            datos.append({
                'Participante': nombre_limpio, 
                'Puntos': p, 
                'Predicción Goles': g_p,
                'Diferencia': dif
            })
            
        # Crear DataFrame y ordenar por Puntos (Desc) y luego Diferencia (Asc)
        df_ranking = pd.DataFrame(datos).sort_values(
            by=['Puntos', 'Diferencia'], 
            ascending=[False, True]
        ).reset_index(drop=True)
        
        df_ranking.index += 1
        df_ranking['Pos'] = df_ranking.index
        # Nueva lógica: TOP 11
        df_ranking['Estado'] = df_ranking['Pos'].apply(lambda x: '✅ TOP 11 - PASA' if x <= 11 else '❌ ELIMINADO')
        
        return df_ranking, goles_reales

    except Exception as e:
        st.error(f"Error al cargar la pestaña '{NOMBRE_PESTANA}': {e}")
        return pd.DataFrame(), 0

# --- EJECUCIÓN ---
df_ranking, goles_totales_reales = cargar_datos()

if not df_ranking.empty:
    # TÍTULO E INFO
    st.title("🏢 World Cup 2026: Leaderboard & Analytics")
    st.subheader(f"🎯 Fase Actual: {NOMBRE_PESTANA}")
    st.write(f"📊 **Goles Reales del Torneo (Celda H36):** {goles_totales_reales}")
    st.markdown("---")
    
    # TARJETAS DEL PODIO
    c1, c2, c3 = st.columns(3)
    for i in range(3):
        if len(df_ranking) > i:
            emoji = ["🥇", "🥈", "🥉"][i]
            color = ["#FFD700", "#C0C0C0", "#CD7F32"][i]
            [c1, c2, c3][i].markdown(f"""
                <div class='metric-card' style='border-color: {color};'>
                    <div class='metric-title'>{emoji} {i+1}ER LUGAR</div>
                    <div style='font-size: 24px; font-weight: bold; color: {color};'>{df_ranking.iloc[i]['Participante']}</div>
                    <div style='font-size: 20px;'>{df_ranking.iloc[i]['Puntos']} pts</div>
                    <div style='font-size: 12px; color: #aaa;'>Dif. Goles: {df_ranking.iloc[i]['Diferencia']}</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # TABLA Y GRÁFICA
    col_tab, col_graf = st.columns([1.2, 2])
    
    with col_tab:
        st.subheader("📋 Clasificación (Top 11)")
        # Solo mostramos columnas clave para la tabla
        st.dataframe(
            df_ranking[['Pos', 'Participante', 'Puntos', 'Diferencia', 'Estado']], 
            use_container_width=True, 
            hide_index=True
        )
        st.info("Criterio de desempate: Cercanía al total real de goles (Celda H36).")
        
    with col_graf:
        st.subheader("📊 Gráfico de Rendimiento")
        fig = px.bar(
            df_ranking, 
            x='Participante', 
            y='Puntos', 
            color='Estado',
            color_discrete_map={'✅ TOP 11 - PASA': '#FFD700', '❌ ELIMINADO': '#444444'},
            category_orders={"Participante": df_ranking['Participante'].tolist()},
            text='Puntos',
            hover_data=['Diferencia']
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)',
            font_color="white", 
            showlegend=True,
            legend_title_text=''
        )
        fig.update_traces(textposition='outside')
        
        # Línea de corte en el puesto 11
        if len(df_ranking) >= 11:
            corte = df_ranking.iloc[10]['Puntos']
            fig.add_hline(y=corte, line_dash="dot", line_color="white", annotation_text="Línea de Corte (11º)")

        st.plotly_chart(fig, use_container_width=True)

    # Botón lateral de actualización
    with st.sidebar:
        if st.button('🔄 Refrescar Datos'):
            st.cache_data.clear()
            st.rerun()

else:
    st.warning(f"Esperando datos en la pestaña '{NOMBRE_PESTANA}'...")
