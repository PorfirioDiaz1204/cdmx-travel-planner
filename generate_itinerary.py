import os
import json
import datetime
from dotenv import load_dotenv
from supabase import create_client, Client
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import List

# 1. Inicializar credenciales
load_dotenv()
load_dotenv("ROOT.env")

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
gemini_key = os.getenv("GEMINI_API_KEY")

if not all([supabase_url, supabase_key, gemini_key]):
    raise ValueError("Faltan variables de entorno en el .env")

supabase: Client = create_client(supabase_url, supabase_key)
ai_client = genai.Client(api_key=gemini_key)

# 2. Esquema de Salida del Itinerario
class Actividad(BaseModel):
    hora_sugerida: str = Field(description="Ejemplo: '09:00 AM', '02:30 PM'")
    lugar_nombre: str = Field(description="Nombre del lugar seleccionado de la base de datos O el nombre de la actividad/compromiso personal especificado por el usuario")
    categoria: str = Field(description="Categoría del lugar (ej. 'Compromiso personal', 'Trabajo', 'Restaurante', 'Museo', 'Excursión / Day-Trip')")
    razon_recomendacion: str = Field(description="Explicación corta de por qué se sugiere en este momento o nota sobre el compromiso personal")

class DiaItinerario(BaseModel):
    dia_numero: int
    fecha: str = Field(description="Formato YYYY-MM-DD")
    dia_semana: str = Field(description="Ejemplo: 'Lunes', 'Martes', etc.")
    titulo_dia: str = Field(description="Ejemplo: 'Día 1: Arte y Cultura en el Centro Histórico'")
    zona_principal: str = Field(description="Zona concentrada del día para minimizar traslados")
    actividades: List[Actividad]

class PlanDeViaje(BaseModel):
    destino: str
    total_dias: int
    resumen_viaje: str = Field(description="Breve introducción del plan personalizado")
    itinerario_diario: List[DiaItinerario]

class ReemplazoRespuesta(BaseModel):
    lugar_nombre: str = Field(description="Nombre exacto del lugar alternativo elegido")
    categoria: str = Field(description="Categoría del lugar seleccionado")
    razon_recomendacion: str = Field(description="Explicación concisa de por qué este nuevo lugar encaja bien en la hora y contexto indicado")

# 3. Función Principal del Generador
def generar_plan(
    destino: str,
    fecha_inicio: datetime.date,
    fecha_fin: datetime.date,
    perfil_grupo: str,
    estilo_viaje: str,
    hora_inicio: str,
    hora_fin: str,
    bloqueos_horario: str = "",
    incluir_escapadas: bool = False
) -> bool:
    num_dias = (fecha_fin - fecha_inicio).days + 1
    print(f"🔍 Consultando Supabase para {destino} ({num_dias} días)...")
    
    # Consulta a la nueva tabla multidestino
    query = supabase.table("lugares_multidestino").select("*").eq("ciudad", destino)
    
    # Excluir escapadas lejanas si la opción no está marcada
    if not incluir_escapadas:
        query = query.eq("es_escapada_fuera", False)
        
    response = query.execute()
    lugares_disponibles = response.data

    if not lugares_disponibles:
        print(f"❌ No se encontraron lugares en la base de datos para {destino}.")
        return False

    prompt = f"""
    Eres un experto guía de viajes internacional.
    Organiza un plan de viaje completo en '{destino}' del {fecha_inicio.strftime('%Y-%m-%d')} al {fecha_fin.strftime('%Y-%m-%d')} ({num_dias} días).
    Perfil del grupo: '{perfil_grupo}'
    Estilo de viaje: '{estilo_viaje}'

    RESTRICCIONES DE TIEMPO Y COMPROMISOS DEL USUARIO:
    - Rango operativo diario predeterminado: De {hora_inicio} a {hora_fin}.
    - COMPROMISOS O MOMENTOS OCUPADOS INDICADOS POR EL USUARIO:
      {bloqueos_horario if bloqueos_horario else 'Ninguno'}.

    Lista de lugares disponibles en la base de datos oficial:
    {json.dumps(lugares_disponibles, ensure_ascii=False)}

    REGLAS ESTRICTAS DE PLANIFICACIÓN:
    1. ORIGEN DE LAS ACTIVIDADES: Utiliza los lugares de la base de datos para los itinerarios turísticos. SIN EMBARGO, si el usuario explícitamente indica un compromiso personal, reunión o evento privado (ej. "comida familiar", "juntas de trabajo"), DEBES INCLUIRLO EXPRESAMENTE como una actividad más dentro del itinerario en su horario correspondiente.
    2. INICIO TARDÍO O TIEMPOS LIBRES: Si el usuario menciona que un día específico desea empezar más tarde (ej. "el sábado empezar a la 1pm"), simplemente programa la primera actividad turística de ese día a esa hora especificada. No agregues bloques artificiales como 'descanso' o 'mañana libre'.
    3. MANEJO DE ESCAPADAS / DAY TRIPS: {'Incluye excursiones o escapadas fuera de la mancha urbana si enriquecen la ruta.' if incluir_escapadas else 'Limítate strictly al área urbana principal.'}
    4. REGLA DEL DÍA DE LA SEMANA Y HORARIOS: Evalúa qué día de la semana cae cada fecha. Si una fecha es LUNES, NO programes museos públicos que cierran. Utiliza parques, mercados, barrios históricos o restaurantes.
    5. Agrupa las actividades de un mismo día en la MISMA ZONA o zonas contiguas para evitar tráfico.
    6. Cada día debe tener entre 3 y 4 actividades organizadas cronológicamente respetando las ventanas de tiempo.
    """

    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=PlanDeViaje,
        temperature=0.3
    )

    print(f"🤖 Generando itinerario inteligente para {destino} con Gemini...")
    
    try:
        res = ai_client.models.generate_content(
            model="gemini-flash-lite-latest",
            contents=prompt,
            config=config,
        )
        
        plan_json = json.loads(res.text)
        
        archivo_salida = "itinerario_generado.json"
        with open(archivo_salida, "w", encoding="utf-8") as f:
            json.dump(plan_json, f, ensure_ascii=False, indent=4)
            
        print(f"✅ ¡Itinerario para {destino} generado con éxito!")
        return True
        
    except Exception as e:
        print(f"❌ Error al generar el itinerario: {e}")
        return False

# 4. Función para reemplazar una actividad específica
def reemplazar_actividad(dia_numero: int, hora_sugerida: str, nombre_lugar_actual: str) -> bool:
    """
    Reemplaza una actividad específica en itinerario_generado.json seleccionando un
    nuevo lugar de la base de datos de Supabase que aún no esté agendado.
    """
    archivo_json = "itinerario_generado.json"
    if not os.path.exists(archivo_json):
        print("❌ No existe el archivo de itinerario generado.")
        return False

    try:
        with open(archivo_json, "r", encoding="utf-8") as f:
            plan = json.load(f)

        destino = plan.get("destino")
        if not destino:
            return False

        # Extraer todos los lugares actualmente usados
        lugares_usados = set()
        for dia in plan.get("itinerario_diario", []):
            for act in dia.get("actividades", []):
                lugares_usados.add(act["lugar_nombre"])

        # Consultar catálogo completo para este destino
        res_db = supabase.table("lugares_multidestino").select("*").eq("ciudad", destino).execute()
        if not res_db.data:
            print(f"❌ No se encontraron lugares en la BD para {destino}.")
            return False

        # Filtrar lugares disponibles excluyendo los que ya están en el plan
        candidatos = [l for l in res_db.data if l["nombre"] not in lugares_usados]

        if not candidatos:
            print("⚠️ No hay lugares disponibles sin usar para reemplazar.")
            return False

        candidatos_resumen = [
            {
                "nombre": c["nombre"],
                "categoria": c.get("categoria"),
                "zona": c.get("zona"),
                "descripcion": c.get("descripcion_corta")
            }
            for c in candidatos
        ]

        prompt_reemplazo = f"""
        Actúa como un guía de viajes experto. Necesitamos reemplazar una actividad del itinerario para {destino}.
        
        Actividad a sustituir:
        - Lugar actual: "{nombre_lugar_actual}"
        - Horario: {hora_sugerida}

        Selecciona la MEJOR opción de la siguiente lista de alternativas disponibles que NO se han usado:
        {json.dumps(candidatos_resumen, ensure_ascii=False)}

        Asegúrate de que la nueva propuesta encaje de manera lógica en ese horario del día.
        """

        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ReemplazoRespuesta,
            temperature=0.3
        )

        res = ai_client.models.generate_content(
            model="gemini-flash-lite-latest",
            contents=prompt_reemplazo,
            config=config
        )

        nuevo_lugar_data = json.loads(res.text)

        # Aplicar el cambio en el JSON
        modificado = False
        for dia in plan.get("itinerario_diario", []):
            if dia.get("dia_numero") == dia_numero:
                for act in dia.get("actividades", []):
                    if act.get("hora_sugerida") == hora_sugerida and act.get("lugar_nombre") == nombre_lugar_actual:
                        act["lugar_nombre"] = nuevo_lugar_data["lugar_nombre"]
                        act["categoria"] = nuevo_lugar_data.get("categoria", act["categoria"])
                        act["razon_recomendacion"] = nuevo_lugar_data.get("razon_recomendacion", "Reemplazo personalizado generado por IA.")
                        modificado = True
                        break

        if modificado:
            with open(archivo_json, "w", encoding="utf-8") as f:
                json.dump(plan, f, ensure_ascii=False, indent=4)
            print(f"✅ Actividad '{nombre_lugar_actual}' reemplazada con éxito por '{nuevo_lugar_data['lugar_nombre']}'")
            return True

        return False

    except Exception as e:
        print(f"❌ Error al reemplazar la actividad: {e}")
        return False