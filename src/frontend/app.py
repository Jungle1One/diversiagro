import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import json
import plotly.express as px
import pandas as pd
from pathlib import Path

# Configuración premium de la página
st.set_page_config(
    page_title="DiversIAgro",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar historial de clics
if 'map_history' not in st.session_state:
    st.session_state.map_history = []

# Inyectar CSS personalizado
BASE_DIR = Path(__file__).resolve().parent
css_path = BASE_DIR / 'assets' / 'css' / 'style.css'
logo_path = BASE_DIR / 'assets' / 'images' / 'logo-diversiagro.png'

if css_path.exists():
    with open(css_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

API_URL = "http://127.0.0.1:8000/api"

def get_prediction(cultivo, lat, lon, altitud, pendiente, lluvia):
    payload = {
        "cultivo": cultivo,
        "lat": lat,
        "lon": lon,
        "altitud_msnm": altitud,
        "pendiente_grados": pendiente,
        "precipitacion_anual_mm": lluvia
    }
    try:
        response = requests.post(f"{API_URL}/predict", json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def get_prediction_from_coords(cultivo, lat, lon):
    payload = {
        "cultivo": cultivo,
        "lat": lat,
        "lon": lon
    }
    try:
        response = requests.post(f"{API_URL}/predict_from_coords", json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def get_municipio_location(municipio_name):
    if municipio_name == "Todos":
        return 3.4372, -76.5225, 8
    try:
        response = requests.get(f"{API_URL}/municipio/{municipio_name}", timeout=30)
        if response.status_code == 200:
            data = response.json()
            return data["lat"], data["lon"], data["zoom"]
    except:
        pass
    return 3.4372, -76.5225, 8

# Header
st.markdown("<h2>DiversIAgro: Diversificación Agrícola con IA</h2>", unsafe_allow_html=True)
st.markdown("Plataforma interactiva para evaluar la aptitud agrícola y explorar **alternativas viables al monocultivo** mediante IA.")

MUNICIPIOS_VALLE = [
    "Todos", "Alcalá", "Andalucía", "Ansermanuevo", "Argelia", "Bolívar", "Buenaventura", 
    "Buga", "Bugalagrande", "Caicedonia", "Cali", "Calima - El Darién", "Candelaria", 
    "Cartago", "Dagua", "El Águila", "El Cairo", "El Cerrito", "El Dovio", "Florida", 
    "Ginebra", "Guacarí", "Jamundí", "La Cumbre", "La Unión", "La Victoria", "Obando", 
    "Palmira", "Pradera", "Restrepo", "Riofrío", "Roldanillo", "San Pedro", "Sevilla", 
    "Toro", "Trujillo", "Tuluá", "Ulloa", "Versalles", "Vijes", "Yotoco", "Yumbo", "Zarzal"
]

# Sidebar
with st.sidebar:
    logo_path = BASE_DIR / 'assets' / 'images' / 'logo-diversiagro.png'
    if logo_path.exists():
        st.image(str(logo_path), width=100)
    else:
        # Fallback si no existe
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Escudo_del_Valle_del_Cauca.svg/1200px-Escudo_del_Valle_del_Cauca.svg.png", width=100)
    st.title("Filtros Geográficos")
    
    departamento = st.selectbox("Departamento", ["Valle del Cauca"])
    municipio = st.selectbox("Municipio", MUNICIPIOS_VALLE)
    


    st.markdown("---")
    modo = st.radio("Módulo de Evaluación", ["Mapa Dinámico (Multicultivo)", "Simulador Climático"])
    st.markdown("---")
    if modo == "Mapa Dinámico (Multicultivo)":
        if st.button("Limpiar Historial del Mapa"):
            st.session_state.map_history = []
            st.session_state.active_point_index = -1
            st.rerun()

        st.markdown("### 📍 Puntos Analizados")
        if len(st.session_state.map_history) == 0:
            st.info("No has seleccionado puntos.")
        else:
            for idx, hist in enumerate(st.session_state.map_history):
                muni_name = hist['res'].get('municipio_detectado', f'Punto {idx+1}')
                is_active = st.session_state.get('active_point_index', len(st.session_state.map_history) - 1) == idx
                btn_label = f"{'👉 ' if is_active else ''}Ver Punto {idx+1}"
                if st.button(btn_label, key=f"hist_btn_{idx}"):
                    st.session_state.active_point_index = idx
                    st.session_state.show_map = False
                    st.rerun()
        st.markdown("---")
    
    if modo == "Simulador Climático":
        st.subheader("Cultivo Objetivo")
        cultivo = st.selectbox("Seleccione Cultivo:", ["Cafe", "Cacao", "Aguacate", "Cana_panelera", "Fresa"]).lower()
        st.subheader("Variables Bioclimáticas")
        altitud = st.slider("Altitud (msnm)", 0, 4000, 1400, 50)
        pendiente = st.slider("Pendiente (°)", 0, 90, 15, 1)
        lluvia = st.slider("Precipitación Anual (mm)", 500, 5000, 1800, 100)
        
        btn_simular = st.button("Ejecutar Simulación")

if modo == "Simulador Climático":
    st.markdown("### Escenario Actual")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Cultivo Seleccionado", cultivo.capitalize())
    col2.metric("Altitud Simulada", f"{altitud} m")
    col3.metric("Lluvia Anual", f"{lluvia} mm")
    
    if 'btn_simular' in locals() and btn_simular:
        lat, lon = 3.9, -76.2
        with st.spinner("Consultando Motor de Inteligencia Artificial..."):
            res = get_prediction(cultivo, lat, lon, altitud, pendiente, lluvia)
            
            if "error" in res:
                st.error(f"Error de conexión con la API: {res['error']}")
            else:
                st.success("Simulación Finalizada")
                final_score = res['final_score']
                label = res['aptitud_label']
                c1, c2, c3 = st.columns(3)
                with c1: st.metric("Puntuación Final (0-3)", f"{final_score:.2f}")
                with c2: st.metric("Aptitud", label.upper())
                with c3: st.metric("Corrección Kriging", f"{res['kriging_correction']:+.2f} pts")

elif modo == "Mapa Dinámico (Multicultivo)":
    st.info("Haga clic en el mapa. Se evaluarán todos los cultivos entrenados simultáneamente para promover la diversificación agrícola.")
    
    start_lat, start_lon, zoom = get_municipio_location(municipio)
    map_key = f"map_{municipio}"
    
    if 'show_map' not in st.session_state:
        st.session_state.show_map = True
        
    # Contenedores para mantener el orden visual
    map_placeholder = st.empty()
    results_placeholder = st.container()

    # 1. Recuperar el estado del mapa
    map_state = st.session_state.get(map_key)
    is_new_click = False
    
    if map_state:
        if map_state.get("last_clicked"):
            lat = map_state["last_clicked"]["lat"]
            lon = map_state["last_clicked"]["lng"]
            
            is_new_click = True
            if len(st.session_state.map_history) > 0:
                last = st.session_state.map_history[-1]
                if abs(last['lat'] - lat) < 0.0001 and abs(last['lon'] - lon) < 0.0001:
                    is_new_click = False
                    
    if is_new_click:
        st.session_state.show_map = False
        map_placeholder.empty() # Forzar a Streamlit a borrar el mapa del navegador instantáneamente
                    
    # 2. Dibujar el mapa (si está visible)
    if st.session_state.show_map:
        with map_placeholder.container():
            m = folium.Map(location=[start_lat, start_lon], zoom_start=zoom, tiles="OpenTopoMap")
            bounds = []
            
            active_idx = st.session_state.get('active_point_index', len(st.session_state.map_history) - 1)
            
            for idx, hist in enumerate(st.session_state.map_history):
                color = "red" if idx == active_idx else "blue"
                muni_text = hist['res'].get('municipio_detectado', 'Desconocido')
                popup_text = f"<b>{muni_text}</b><br>Lat: {hist['lat']:.4f}<br>Lon: {hist['lon']:.4f}"
                
                folium.Marker(
                    [hist['lat'], hist['lon']],
                    popup=folium.Popup(popup_text, max_width=200),
                    icon=folium.Icon(color=color, icon="info-sign")
                ).add_to(m)
                bounds.append([hist['lat'], hist['lon']])
                
            if len(bounds) > 0:
                m.fit_bounds(bounds, max_zoom=13)
                
            st_folium(m, use_container_width=True, height=500, returned_objects=["last_clicked"], key=map_key)

    # 3. Mostrar resultados y procesar clics
    with results_placeholder:
        if not st.session_state.show_map:
            if st.button("🗺️ Volver al Mapa para buscar otro punto", use_container_width=True):
                st.session_state.show_map = True
                st.rerun()
                
        if is_new_click:
            import time
            import streamlit.components.v1 as components
            # Inyectar script de scroll inmediato
            components.html(
                f"""
                <script>
                setTimeout(function() {{
                    const mainContainer = window.parent.document.querySelector('.main') || window.parent.document.querySelector('section.main') || window.parent.document.querySelector('.stAppViewContainer');
                    if (mainContainer) {{
                        mainContainer.scrollTo({{
                            top: mainContainer.scrollHeight,
                            behavior: 'smooth'
                        }});
                    }} else {{
                        window.parent.scrollTo({{
                            top: window.parent.document.body.scrollHeight,
                            behavior: 'smooth'
                        }});
                    }}
                }}, 100);
                </script>
                """,
                height=0
            )

            st.markdown("---")
            geo_placeholder = st.empty()
            st.markdown("### 🌾 Evaluación de Diversificación")
            cards_container = st.container()
            with cards_container:
                cols = st.columns(5)
                
            with st.status("🌍 Analizando coordenadas espaciales...", expanded=True) as status:
                st.write(f"📍 Punto detectado: {lat:.4f}, {lon:.4f}")
                st.write("📡 Extrayendo elevación, pendiente y lluvia anual...")
                st.write("🧠 Ejecutando modelo RFRK Multicultivo...")
                
                CULTIVOS = ["cafe", "cacao", "aguacate", "cana_panelera", "fresa"]
                resultados = []
                gis_data = None
                
                # Fetch predictions crop by crop dynamically
                for i, cultivo in enumerate(CULTIVOS):
                    st.write(f"⏳ Evaluando **{cultivo.upper()}** ({i+1}/{len(CULTIVOS)})...")
                    res = get_prediction_from_coords(cultivo, lat, lon)
                    
                    if "error" not in res:
                        resultados.append({
                            "cultivo": res["cultivo"],
                            "rf_score": res["rf_score"],
                            "kriging_correction": res["kriging_correction"],
                            "final_score": res["final_score"],
                            "aptitud_label": res["aptitud_label"]
                        })
                        
                        if gis_data is None:
                            gis_data = {
                                "municipio_detectado": res["municipio_detectado"],
                                "altitud_extraida": res["altitud_extraida"],
                                "pendiente_extraida": res["pendiente_extraida"],
                                "lluvia_extraida": res["lluvia_extraida"]
                            }
                            with geo_placeholder.container():
                                st.markdown(f"### 📍 Resultados Geográficos: {gis_data['municipio_detectado']}")
                                c1, c2, c3 = st.columns(3)
                                c1.metric("Altitud (DEM)", f"{gis_data['altitud_extraida']:.1f} m")
                                c2.metric("Pendiente (DEM)", f"{gis_data['pendiente_extraida']:.1f}°")
                                c3.metric("Lluvia (IDEAM)", f"{gis_data['lluvia_extraida']:.1f} mm")
                                
                        with cols[i]:
                            st.info(f"**{res['cultivo'].upper()}**")
                            st.metric("Puntaje", f"{res['final_score']:.2f} / 3.0")
                            st.write(f"*{res['aptitud_label']}*")
                    else:
                        st.error(f"Error evaluando {cultivo}: {res['error']}")
                
                if resultados and gis_data:
                    resultados.sort(key=lambda x: x['final_score'], reverse=True)
                    final_res = {
                        "lat": lat, "lon": lon,
                        "municipio_detectado": gis_data["municipio_detectado"],
                        "altitud_extraida": gis_data["altitud_extraida"],
                        "pendiente_extraida": gis_data["pendiente_extraida"],
                        "lluvia_extraida": gis_data["lluvia_extraida"],
                        "resultados": resultados
                    }
                    st.session_state.map_history.append({'lat': lat, 'lon': lon, 'res': final_res})
                    st.session_state.active_point_index = len(st.session_state.map_history) - 1
                    status.update(label="Análisis completado con éxito", state="complete", expanded=False)
                else:
                    status.update(label="Error en el servidor GIS", state="error", expanded=False)
                    st.error("No se pudieron obtener resultados para los cultivos.")
            
            time.sleep(1)
            st.rerun()

        if len(st.session_state.map_history) > 0 and not st.session_state.show_map:
            active_idx = st.session_state.get('active_point_index', len(st.session_state.map_history) - 1)
            # Asegurar rango
            if active_idx >= len(st.session_state.map_history) or active_idx < 0:
                active_idx = len(st.session_state.map_history) - 1
                
            latest = st.session_state.map_history[active_idx]['res']
            
            st.markdown("---")
            st.markdown(f"### 📍 Resultados Geográficos: {latest['municipio_detectado']}")
            c1, c2, c3 = st.columns(3)
            c1.metric("Altitud (DEM)", f"{latest['altitud_extraida']:.1f} m")
            c2.metric("Pendiente (DEM)", f"{latest['pendiente_extraida']:.1f}°")
            c3.metric("Lluvia (IDEAM)", f"{latest['lluvia_extraida']:.1f} mm")
            
            st.markdown("### 🌾 Evaluación de Diversificación")
            
            resultados = latest['resultados']
            df_res = pd.DataFrame(resultados)
            
            cols = st.columns(len(resultados))
            for i, row in enumerate(resultados):
                with cols[i]:
                    st.info(f"**{row['cultivo'].upper()}**")
                    st.metric("Puntaje", f"{row['final_score']:.2f} / 3.0")
                    st.write(f"*{row['aptitud_label']}*")
                    
            fig = px.bar(
                df_res, 
                x='cultivo', 
                y='final_score', 
                color='cultivo',
                text_auto='.2f',
                title='Comparativa de Aptitud por Cultivo',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig.update_layout(yaxis_range=[0, 3], paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
            st.plotly_chart(fig, use_container_width=True)

            # Inyectar animación para hacer scroll
            import time
            import streamlit.components.v1 as components
            components.html(
                f"""
                <script>
                setTimeout(function() {{
                    const mainContainer = window.parent.document.querySelector('.main') || window.parent.document.querySelector('section.main') || window.parent.document.querySelector('.stAppViewContainer');
                    if (mainContainer) {{
                        mainContainer.scrollTo({{
                            top: mainContainer.scrollHeight,
                            behavior: 'smooth'
                        }});
                    }} else {{
                        window.parent.scrollTo({{
                            top: window.parent.document.body.scrollHeight,
                            behavior: 'smooth'
                        }});
                    }}
                }}, 300); // {time.time()}
                </script>
                """,
                height=0
            )
