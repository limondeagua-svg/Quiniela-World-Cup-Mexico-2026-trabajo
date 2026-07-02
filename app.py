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
            border: 2px solid #FFD700;
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

@st.cache_data(ttl=10)
def cargar_datos():
    try:
        # Cargar la pestaña específica
        df = pd.read_excel(archivo, sheet_name=NOMBRE_PESTANA, header=None, dtype=str)
        
        # --- REFERENCIAS AJUSTADAS ---
        # Goles Reales: Celda H36 -> Fila índice 35, Columna índice 7 (H)
        try:
            goles_reales = int(float(df.iloc[35, 7]))
        except:
            goles_reales = 0

        # Nombres: Fila 2 (index 1), Columna I en adelante (index 8)
        nombres = df.iloc[1, 8:].tolist()
        # Puntos: Fila 3 (index 2), Columna I en adelante (index 8)
        puntos = df.iloc[2, 8:].tolist()
        # Predicciones Goles: Fila 36 (index 35), Columna I en adelante (index 8)
        pred_goles = df.iloc[35, 8:].tolist()
        
        datos = []
        for i in range(len(nombres)):
            nombre_limpio = str(nombres[i]).strip()
            
            # Filtramos celdas vacías o que no sean participantes
            if nombre_limpio == 'nan' or not nombre_limpio or nombre_limpio == 'None':
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
                'Diferencia': dif
            })
            
        # Crear DataFrame y ordenar por Puntos (Desc) y luego Diferencia (Asc)
        df_ranking = pd.DataFrame(datos)
        
        if not df_ranking.empty:
            df_ranking = df_ranking.sort_values(
                by=['Puntos', 'Diferencia'], 
                ascending=[False, True]
            ).reset_index(drop=True)
            
            df_ranking.index += 1
            df_ranking['Pos'] = df_ranking.index
            # Nueva lógica: TOP 11
            df_ranking['Estado'] = df_ranking['Pos'].apply(lambda x: '✅ TOP 11' if x <= 11 else '❌ ELIMINADO')
        
        return df_ranking, goles_reales

    except Exception as e:
        st.error(f"Error al cargar la pestaña '{NOMBRE_PESTANA}': {e}")
        return pd.DataFrame(), 0

# --- EJECUCIÓN ---
df_ranking, goles_totales_reales = cargar_datos()

if not df_ranking.empty:
    st.title("🏆 World Cup 2026: Leaderboard & Analytics")
    st.subheader(f"🎯 Fase Actual: {NOMBRE_PESTANA}")
    st.write(f"📊 **Goles Reales del Torneo (Celda H36):** {goles_totales_reales}")
    st.markdown("---")
    
    # TARJETAS DEL PODIO (1ro al Centro, 2do Izquierda, 3ro Derecha)
    c1, c2, c3 = st.columns(3)
    
    # 2do Lugar
    with c1:
        if len(df_ranking) >= 2:
            st.markdown(f"""
                <div class='metric-card' style='border-color: #C0C0C0; margin-top: 25px;'>
                    <div class='metric-title'>🥈 2DO LUGAR</div>
                    <div style='font-size: 22px; font-weight: bold; color: #C0C0C0;'>{df_ranking.iloc[1]['Participante']}</div>
                    <div style='font-size: 20px;'>{df_ranking.iloc[1]['Puntos']} pts</div>
                    <div style='font-size: 12px; color: #aaa;'>Dif. Goles: {df_ranking.iloc[1]['Diferencia']}</div>
                </div>
            """, unsafe_allow_html=True)

    # 1er Lugar
    with c2:
        st.markdown(f"""
            <div class='metric-card' style='border-width: 4px; box-shadow: 0px 0px 15px #FFD700;'>
                <div class='metric-title'>🥇 1ER LUGAR</div>
                <div style='font-size: 28px; font-weight: bold; color: #FFD700;'>{df_ranking.iloc[0]['Participante']}</div>
                <div style='font-size: 22px;'>{df_ranking.iloc[0]['Puntos']} pts</div>
                <div style='font-size: 12px; color: #aaa;'>Dif. Goles: {df_ranking.iloc[0]['Diferencia']}</div>
            </div>
        """, unsafe_allow_html=True)

    # 3er Lugar
    with c3:
        if len(df_ranking) >= 3:
            st.markdown(f"""
                <div class='podium-card' style='border: 2px solid #CD7F32; padding: 20px; border-radius: 10px; text-align: center; color: #CD7F32; margin-top: 45px;'>
                    <div style='font-size: 14px; color: #aaa;'>🥉 3ER LUGAR</div>
                    <div style='font-size: 18px; font-weight: bold;'>{df_ranking.iloc[2]['Participante']}</div>
                    <div style='font-size: 18px;'>{df_ranking.iloc[2]['Puntos']} pts</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # TABLA Y GRÁFICA
    col_tab, col_graf = st.columns([1, 2])
    
    with col_tab:
        st.subheader("📋 Clasificación Oficial")
        st.dataframe(
            df_ranking[['Pos', 'Participante', 'Puntos', 'Diferencia', 'Estado']], 
            use_container_width=True, 
            hide_index=True
        )
        st.info("Desempate: El que más se acerca a los goles reales (H36).")
        
    with col_graf:
        st.subheader("📊 Gráfico de Rendimiento")
        fig = px.bar(
            df_ranking, 
            x='Participante', 
            y='Puntos', 
            color='Estado',
            color_discrete_map={'✅ TOP 11': '#FFD700', '❌ ELIMINADO': '#444444'},
            text='Puntos'
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)',
            font_color="white", 
            showlegend=True
        )
        
        # Línea de corte en el puesto 11
        if len(df_ranking) >= 11:
            corte = df_ranking.iloc[10]['Puntos']
            fig.add_hline(y=corte, line_dash="dot", line_color="white", annotation_text="Línea de Corte")

        st.plotly_chart(fig, use_container_width=True)

    with st.sidebar:
        if st.button('🔄 Refrescar Datos'):
            st.cache_data.clear()
            st.rerun()

else:
    st.warning(f"No se encontraron datos en la pestaña '{NOMBRE_PESTANA}'. Revisa la columna I en adelante.")
