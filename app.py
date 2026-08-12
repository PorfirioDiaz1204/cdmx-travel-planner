import streamlit as st
import json
import os
import datetime
import folium
from streamlit_folium import st_folium
from generate_itinerary import generar_plan, supabase
from exporter import generar_pdf, generar_txt

st.set_page_config(
    page_title="Multi-City Travel Planner",
    page_icon="🗺️",
    layout="wide"
)

st.title("🗺️ Smart Travel Assistant")
st.subheader("Itinerarios inteligentes personalizados con optimización geográfica")

# Configuración de ciudades piloto
CIUDADES_PILOTO = {
    "Ciudad de México": {"lat": 19.4326, "lon": -99.1332, "es_hub": False},
    "Mérida": {"lat": 20.9676, "lon": -89.6237, "es_hub": True},
    "Barcelona": {"lat": 41.3851, "lon": 2.1734, "es_hub": True},
    "Cusco": {"lat": -13.5319, "lon": -71.9675, "es_hub": True}
}

# 1. Barra lateral
with st.sidebar:
    st.header("⚙️ Configura tu Viaje")
    
    destino_seleccionado = st.selectbox(
        "📍 Selecciona tu Destino",
        options=list(CIUDADES_PILOTO.keys())
    )
    
    # Mostrar opción de escapadas si el destino es una ciudad Hub
    es_hub = CIUDADES_PILOTO[destino_seleccionado]["es_hub"]
    incluir_escapadas = False
    
    if es_hub:
        st.info(f"💡 {destino_seleccionado} funciona como base para explorar zonas cercanas.")
        incluir_escapadas = st.checkbox(
            "¿Incluir escapadas / day-trips fuera de la ciudad?",
            value=True
        )

    hoy = datetime.date.today()
    fechas = st.date_input(
        "¿Cuáles son las fechas de tu viaje?",
        value=(hoy, hoy + datetime.timedelta(days=2)),
        min_value=hoy,
        format="DD/MM/YYYY"
    )
    
    perfil = st.selectbox(
        "¿Con quién viajas?",
        ["Familia con niños", "Pareja", "Solo / Mochilero", "Grupo de Amigos"]
    )
    
    estilo = st.multiselect(
        "¿Qué tipo de actividades buscas?",
        [
            "Café de especialidad", 
            "Museos y Arte", 
            "Hiking y Naturaleza", 
            "Gastronomía Tradicional", 
            "Lujo y Gourmet",
            "Vida Nocturna y Bares",
            "Mercados Locales",
            "Excursión / Day-Trip"
        ],
        default=["Café de especialidad", "Museos y Arte", "Gastronomía Tradicional"]
    )

    st.markdown("---")
    st.subheader("⏰ Control de Horarios")

    col_h1, col_h2 = st.columns(2)
    with col_h1:
        hora_inicio = st.time_input("Inicio del día", value=datetime.time(9, 0))
    with col_h2:
        hora_fin = st.time_input("Fin del día", value=datetime.time(20, 0))

    bloqueos = st.text_area(
        "Horarios ocupados o compromisos",
        placeholder="Ej: El lunes de 2 PM a 5 PM tengo una comida familiar."
    )
    
    btn_generar = st.button("🚀 Generar Itinerario", type="primary")

# 2. Generación al presionar el botón
if btn_generar:
    if isinstance(fechas, tuple) and len(fechas) == 2:
        fecha_inicio, fecha_fin = fechas
        estilo_str = ", ".join(estilo)
        
        with st.spinner(f"🤖 Optimizando ruta para {destino_seleccionado}..."):
            exito = generar_plan(
                destino=destino_seleccionado,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                perfil_grupo=perfil,
                estilo_viaje=estilo_str,
                hora_inicio=hora_inicio.strftime("%I:%M %p"),
                hora_fin=hora_fin.strftime("%I:%M %p"),
                bloqueos_horario=bloqueos,
                incluir_escapadas=incluir_escapadas
            )
            if exito:
                st.session_state["itinerario_listo"] = True
                st.rerun()
            else:
                st.error("Ocurrió un error al generar el itinerario. Revisa la consola.")
    else:
        st.error("Por favor selecciona un rango válido de fechas (entrada y salida).")

# 3. Mostrar el itinerario
archivo_itinerario = "itinerario_generado.json"

if os.path.exists(archivo_itinerario):
    try:
        with open(archivo_itinerario, "r", encoding="utf-8") as f:
            plan = json.load(f)
            
        destino_plan = plan.get('destino', destino_seleccionado)
        st.success(f"¡Itinerario cargado para {destino_plan}!")
        st.write(f"**Resumen:** {plan.get('resumen_viaje')}")
        
        # Consultar lugares de la ciudad correspondiente
        res_lugares = supabase.table("lugares_multidestino").select("*").eq("ciudad", destino_plan).execute()
        dict_lugares = {l['nombre']: l for l in res_lugares.data}
        
        titulos_tabs = [f"Día {d['dia_numero']} ({d.get('fecha', '')})" for d in plan['itinerario_diario']]
        dias_tabs = st.tabs(titulos_tabs)
        
        coords_default = CIUDADES_PILOTO.get(destino_plan, {"lat": 19.4326, "lon": -99.1332})
        
        for i, dia in enumerate(plan['itinerario_diario']):
            with dias_tabs[i]:
                st.markdown(f"### {dia['titulo_dia']} — *{dia.get('dia_semana', '')}*")
                st.caption(f"📍 Zona principal: {dia['zona_principal']}")
                
                col_actividades, col_mapa = st.columns([1, 1])
                
                with col_actividades:
                    for act in dia['actividades']:
                        with st.expander(f"⏰ {act['hora_sugerida']} - {act['lugar_nombre']}", expanded=True):
                            st.write(f"**Categoría:** {act['categoria'].capitalize()}")
                            st.write(f"**Por qué ir:** {act['razon_recomendacion']}")
                            
                with col_mapa:
                    m = folium.Map(location=[coords_default["lat"], coords_default["lon"]], zoom_start=11)
                    
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

        # --- SECCIÓN DE EXPORTACIÓN Y DESCARGAS ---
        st.divider()
        st.markdown("### 📥 Descargar tu Itinerario")
        
        datos_exportar = {
            "dias": [
                {
                    "dia": f"{d['dia_numero']} ({d.get('dia_semana', '')} {d.get('fecha', '')})",
                    "actividades": [
                        {
                            "hora": act["hora_sugerida"],
                            "lugar": act["lugar_nombre"],
                            "descripcion": act["razon_recomendacion"]
                        } for act in d["actividades"]
                    ]
                } for d in plan.get("itinerario_diario", [])
            ]
        }

        col_pdf, col_txt = st.columns(2)

        nombre_archivo_limpio = destino_plan.lower().replace(' ', '_')

        with col_pdf:
            pdf_bytes = generar_pdf(datos_exportar, titulo=f"Itinerario - {destino_plan}")
            st.download_button(
                label="📄 Descargar como PDF",
                data=pdf_bytes,
                file_name=f"itinerario_{nombre_archivo_limpio}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        with col_txt:
            txt_bytes = generar_txt(datos_exportar)
            st.download_button(
                label="📝 Descargar como Texto (.txt)",
                data=txt_bytes,
                file_name=f"itinerario_{nombre_archivo_limpio}.txt",
                mime="text/plain",
                use_container_width=True
            )

    except Exception as e:
        st.error(f"Error al cargar el itinerario visual: {e}")