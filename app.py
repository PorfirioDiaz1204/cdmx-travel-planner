import streamlit as st
import json
import os
import folium
from streamlit_folium import st_folium
from generate_itinerary import generar_plan, supabase

st.set_page_config(
    page_title="CDMX Travel Planner",
    page_icon="🗺️",
    layout="wide"
)

st.title("🗺️ CDMX Travel Assistant-¿Qué onda cachorra? presenta a tu amiga de los lunares, helloow")
st.subheader("Tu itinerario inteligente y personalizado por la Ciudad de México")

# 1. Barra lateral
with st.sidebar:
    st.header("⚙️ Configura tu Viaje")
    
    dias = st.slider("¿Cuántos días estarás en CDMX?", min_value=1, max_value=5, value=3)
    
    perfil = st.selectbox(
        "¿Con quién viajas?",
        ["Familia con niños", "Pareja", "Solo / Mochilero", "Grupo de Amigos"]
    )
    
    estilo = st.multiselect(
        "¿Qué tipo de actividades buscas?",
        ["Café de especialidad", "Museos y Arte", "Hiking y Naturaleza", "Gastronomía Tradicional", "Lujo y Gourmet"],
        default=["Café de especialidad", "Museos y Arte", "Hiking y Naturaleza"]
    )
    
    btn_generar = st.button("🚀 Generar Itinerario", type="primary")

# 2. Generación al presionar el botón
if btn_generar:
    estilo_str = ", ".join(estilo)
    with st.spinner("🤖 Consultando lugares en Supabase y optimizando rutas con IA..."):
        generar_plan(dias=dias, perfil_grupo=perfil, estilo_viaje=estilo_str)
        st.session_state["itinerario_listo"] = True

# 3. Mostrar el itinerario si existe el archivo (independiente de las recargas)
archivo_itinerario = "itinerario_generado.json"

if os.path.exists(archivo_itinerario):
    try:
        with open(archivo_itinerario, "r", encoding="utf-8") as f:
            plan = json.load(f)
            
        st.success("¡Itinerario cargado!")
        st.write(f"**Resumen:** {plan.get('resumen_viaje')}")
        
        # Consultar coordenadas
        res_lugares = supabase.table("lugares_cdmx").select("*").execute()
        dict_lugares = {l['nombre']: l for l in res_lugares.data}
        
        dias_tabs = st.tabs([f"Día {d['dia_numero']}" for d in plan['itinerario_diario']])
        
        for i, dia in enumerate(plan['itinerario_diario']):
            with dias_tabs[i]:
                st.markdown(f"### {dia['titulo_dia']}")
                st.caption(f"📍 Zona principal: {dia['zona_principal']}")
                
                col_actividades, col_mapa = st.columns([1, 1])
                
                with col_actividades:
                    for act in dia['actividades']:
                        with st.expander(f"⏰ {act['hora_sugerida']} - {act['lugar_nombre']}", expanded=True):
                            st.write(f"**Categoría:** {act['categoria'].capitalize()}")
                            st.write(f"**Por qué ir:** {act['razon_recomendacion']}")
                            
                with col_mapa:
                    m = folium.Map(location=[19.4326, -99.1332], zoom_start=12)
                    
                    for act in dia['actividades']:
                        nombre = act['lugar_nombre']
                        if nombre in dict_lugares:
                            lugar_info = dict_lugares[nombre]
                            lat = lugar_info['latitud']
                            lon = lugar_info['longitud']
                            
                            folium.Marker(
                                [lat, lon],
                                popup=nombre,
                                tooltip=f"{act['hora_sugerida']}: {nombre}",
                                icon=folium.Icon(color="red", icon="info-sign")
                            ).add_to(m)
                            
                    st_folium(m, width=450, height=350, key=f"mapa_dia_{dia['dia_numero']}")

    except Exception as e:
        st.error(f"Error al cargar el itinerario visual: {e}")