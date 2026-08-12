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
    lugar_nombre: str = Field(description="Nombre del lugar seleccionado de la base de datos")
    categoria: str = Field(description="Categoría del lugar")
    razon_recomendacion: str = Field(description="Explicación corta de por qué se sugiere en este momento")

class DiaItinerario(BaseModel):
    dia_numero: int
    fecha: str = Field(description="Formato YYYY-MM-DD")
    dia_semana: str = Field(description="Ejemplo: 'Lunes', 'Martes', etc.")
    titulo_dia: str = Field(description="Ejemplo: 'Día 1: Arte y Cultura en el Centro Histórico'")
    zona_principal: str = Field(description="Zona concentrada del día para minimizar traslados")
    actividades: List[Actividad]

class PlanDeViaje(BaseModel):
    destino: str = "Ciudad de México"
    total_dias: int
    resumen_viaje: str = Field(description="Breve introducción del plan personalizado")
    itinerario_diario: List[DiaItinerario]

# 3. Función Principal del Generador
def generar_plan(
    fecha_inicio: datetime.date,
    fecha_fin: datetime.date,
    perfil_grupo: str,
    estilo_viaje: str,
    hora_inicio: str,
    hora_fin: str,
    bloqueos_horario: str = ""
) -> bool:
    num_dias = (fecha_fin - fecha_inicio).days + 1
    print(f"🔍 Consultando base de datos en Supabase para un viaje del {fecha_inicio} al {fecha_fin} ({num_dias} días)...")
    
    # Obtener lugares desde Supabase
    response = supabase.table("lugares_cdmx").select("*").execute()
    lugares_disponibles = response.data

    if not lugares_disponibles:
        print("❌ No se encontraron lugares en la base de datos.")
        return False

    prompt = f"""
    Eres un experto guía de viajes en la Ciudad de México.
    Organiza un plan de viaje completo del {fecha_inicio.strftime('%Y-%m-%d')} al {fecha_fin.strftime('%Y-%m-%d')} ({num_dias} días).
    Perfil del grupo: '{perfil_grupo}'
    Estilo de viaje: '{estilo_viaje}'

    RESTRICCIONES DE TIEMPO DEL USUARIO:
    - Rango operativo diario predeterminado: De {hora_inicio} a {hora_fin}.
    - Compromisos o momentos ocupados indicados expresamente por el usuario:
      {bloqueos_horario if bloqueos_horario else 'Ninguno'}.

    Lista de lugares disponibles en la base de datos:
    {json.dumps(lugares_disponibles, ensure_ascii=False)}

    REGLAS ESTRICTAS DE PLANIFICACIÓN:
    1. Utiliza ÚNICAMENTE los lugares proporcionados en la lista anterior.
    2. REGLA DEL DÍA DE LA SEMANA Y HORARIOS: Evalúa qué día de la semana cae cada fecha. Si una fecha es LUNES, NO programes museos públicos (casi todos cierran). Utiliza parques, mercados, barrios históricos o restaurantes.
    3. Respeta rigurosamente los momentos ocupados indicados por el usuario dejando esa franja libre o ajustando la hora de inicio/fin del día específico según lo solicitado.
    4. Agrupa las actividades de un mismo día en la MISMA ZONA o zonas contiguas para evitar tráfico.
    5. Cada día debe tener entre 3 y 4 actividades organizadas cronológicamente respetando los límites de horario.
    """

    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=PlanDeViaje,
        temperature=0.3,
    )

    print("🤖 Generando itinerario inteligente con Gemini...")
    
    try:
        res = ai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=config,
        )
        
        plan_json = json.loads(res.text)
        
        archivo_salida = "itinerario_generado.json"
        with open(archivo_salida, "w", encoding="utf-8") as f:
            json.dump(plan_json, f, ensure_ascii=False, indent=4)
            
        print(f"✅ ¡Itinerario generado con éxito y guardado en '{archivo_salida}'!")
        return True
        
    except Exception as e:
        print(f"❌ Error al generar el itinerario: {e}")
        return False