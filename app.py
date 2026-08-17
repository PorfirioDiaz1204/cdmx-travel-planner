import streamlit as st
import json
import os
import datetime
import folium
from streamlit_folium import st_folium
from generate_itinerary import generar_plan, reemplazar_actividad, supabase
from autogenerar_lugares import autogenerar_y_poblar
from exporter import generar_pdf, generar_txt

st.set_page_config(
    page_title="Multi-City Travel Planner",
    page_icon="🗺️",
    layout="wide"
)

st.title("🗺️ Smart Travel Assistant")
st.subheader("Itinerarios inteligentes personalizados con optimización geográfica")

# --- OBTENER CIUDADES EXISTENTES DESDE SUPABASE ---
@st.cache_data(ttl=60)
def obtener_ciudades_bd():
    try:
        res = supabase.table("lugares_multidestino").select("ciudad").execute()
        if res.data:
            # Obtener ciudades únicas y ordenarlas
            ciudades = sorted(list(set(l["ciudad"] for l in res.data if l.get("ciudad"))))
            return ciudades
    except Exception as e:
        print(f"Error al obtener ciudades de Supabase: {e}")
    return ["Ciudad de México", "Mérida", "Barcelona", "Cusco"]

ciudades_bd = obtener_ciudades_bd()
opciones_menu = ciudades_bd + ["Otra ciudad..."]

# 1. Barra lateral
with st.sidebar:
    st.header("⚙️ Configura tu Viaje")
    
    opcion_ciudad = st.selectbox(
        "📍 Selecciona tu Destino",
        options=opciones_menu
    )
    
    if opcion_ciudad == "Otra ciudad...":
        destino_seleccionado = st.text_input("Escribe el nombre de la ciudad:", value="Roma").strip()
    else:
        destino_seleccionado = opcion_ciudad

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
    if not destino_seleccionado:
        st.error("Por favor ingresa o selecciona un destino válido.")
    elif isinstance(fechas, tuple) and len(fechas) == 2:
        fecha_inicio, fecha_fin = fechas
        estilo_str = ", ".join(estilo)
        num_dias = (fecha_fin - fecha_inicio).days + 1
        
        # Meta deseada de lugares en la base de datos para garantizar variabilidad
        CANTIDAD_A_GENERAR = 30
        
        # Conversión segura de horarios para evitar TypeError
        h_inicio_str = hora_inicio.strftime("%I:%M %p") if isinstance(hora_inicio, datetime.time) else str(hora_inicio)
        h_fin_str = hora_fin.strftime("%I:%M %p") if isinstance(hora_fin, datetime.time) else str(hora_fin)
        
        with st.status(f"🔎 Preparando datos para **{destino_seleccionado}**...", expanded=True) as status:
            # Check en Supabase
            res_lugares = supabase.table("lugares_multidestino").select("nombre").eq("ciudad", destino_seleccionado).execute()
            cantidad_actual = len(res_lugares.data) if res_lugares.data else 0
            
            if cantidad_actual < CANTIDAD_A_GENERAR:
                faltantes = CANTIDAD_A_GENERAR - cantidad_actual
                status.write(f"🌐 Encontrados {cantidad_actual} lugares. Explorando {faltantes} nuevos lugares...")
                exito_poblar = autogenerar_y_poblar(ciudad=destino_seleccionado, cantidad=faltantes)
                if not exito_poblar:
                    st.warning("No se pudieron autogenerar lugares adicionales, se intentará usar los existentes.")
            else:
                status.write(f"✅ ¡Catálogo suficiente encontrado ({cantidad_actual} lugares disponibles)!")

            status.write(f"🤖 Optimizando ruta de {num_dias} día(s)...")
            exito = generar_plan(
                destino=destino_seleccionado,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                perfil_grupo=perfil,
                estilo_viaje=estilo_str,
                hora_inicio=h_inicio_str,
                hora_fin=h_fin_str,
                bloqueos_horario=bloqueos,
                incluir_escapadas=incluir_escapadas
            )
            
            if exito:
                # Limpiar la caché para actualizar la lista de ciudades disponibles
                st.cache_data.clear()
                status.update(label="¡Itinerario listo!", state="complete")
                st.session_state["itinerario_listo"] = True
                st.rerun()
                
            else:
                status.update(label="Error al generar el itinerario", state="error")
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
        st.success(f"¡Itinerario cargado para **{destino_plan}**!")
        st.write(f"**Resumen:** {plan.get('resumen_viaje')}")
        
        # Consultar lugares de la ciudad correspondiente
        res_lugares = supabase.table("lugares_multidestino").select("*").eq("ciudad", destino_plan).execute()
        dict_lugares = {l['nombre']: l for l in res_lugares.data} if res_lugares.data else {}
        
        # Calcular centro dinámico del mapa (promedio de coords)
        lats = [l['latitud'] for l in res_lugares.data if 'latitud' in l and l['latitud']] if res_lugares.data else []
        lons = [l['longitud'] for l in res_lugares.data if 'longitud' in l and l['longitud']] if res_lugares.data else []
        
        lat_centro = sum(lats) / len(lats) if lats else 19.4326
        lon_centro = sum(lons) / len(lons) if lons else -99.1332

        titulos_tabs = [f"Día {d['dia_numero']} ({d.get('fecha', '')})" for d in plan['itinerario_diario']]
        dias_tabs = st.tabs(titulos_tabs)
        
        for i, dia in enumerate(plan['itinerario_diario']):
            with dias_tabs[i]:
                st.markdown(f"### {dia['titulo_dia']} — *{dia.get('dia_semana', '')}*")
                st.caption(f"📍 Zona principal: {dia['zona_principal']}")
                
                col_actividades, col_mapa = st.columns([1, 1])
                
                with col_actividades:
                    for act_idx, act in enumerate(dia['actividades']):
                        with st.expander(f"⏰ {act['hora_sugerida']} - {act['lugar_nombre']}", expanded=True):
                            st.write(f"**Categoría:** {act['categoria'].capitalize()}")
                            st.write(f"**Por qué ir:** {act['razon_recomendacion']}")
                            
                            # Botón para solicitar reemplazo de esta actividad
                            key_btn = f"swap_{dia['dia_numero']}_{act_idx}_{act['lugar_nombre']}"
                            if st.button("🔄 Cambiar esta actividad", key=key_btn):
                                with st.spinner("Buscando un reemplazo adecuado..."):
                                    ok = reemplazar_actividad(
                                        dia_numero=dia['dia_numero'],
                                        hora_sugerida=act['hora_sugerida'],
                                        nombre_lugar_actual=act['lugar_nombre']
                                    )
                                    if ok:
                                        st.success("¡Actividad actualizada!")
                                        st.rerun()
                                    else:
                                        st.warning("No hay más lugares disponibles en la base de datos para reemplazar esta actividad.")

                with col_mapa:
                    m = folium.Map(location=[lat_centro, lon_centro], zoom_start=12)
                    
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