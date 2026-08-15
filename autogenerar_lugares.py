# autogenerar_lugares.py
import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from supabase import create_client, Client

load_dotenv()

supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
ai_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class Lugar(BaseModel):
    nombre: str
    ciudad: str = Field(description="DEBE SER EXACTAMENTE la ciudad base enviada en el prompt.")
    categoria: str = Field(description="Opciones: Museos y Arte, Gastronomía Tradicional, Café de especialidad, Mercados Locales, Hiking y Naturaleza, Lujo y Gourmet, Excursión / Day-Trip")
    zona: str = Field(description="Nombre del barrio, zona de la ciudad o el municipio/pueblo externo si es escapada.")
    es_escapada_fuera: bool = Field(description="True si está fuera de la mancha urbana / requiere viaje en carretera o tren.")
    latitud: float
    longitud: float
    descripcion_corta: str
    costo_estimado: str = Field(description="Opciones: Gratis, Económico, Moderado, Alto")
    perfil_recomendado: str = Field(description="Combinación de: Familia, Pareja, Solo, Amigos")

class ListaLugares(BaseModel):
    lugares: list[Lugar]

def autogenerar_y_poblar(ciudad: str, cantidad: int = 20) -> bool:
    """Genera nuevos lugares con Gemini y los inserta en Supabase."""
    try:
        # 1. Obtener existentes para no duplicar
        res_db = supabase.table("lugares_multidestino").select("nombre").eq("ciudad", ciudad).execute()
        existentes = [item["nombre"] for item in res_db.data]

        # 2. Diseñar Prompt
        prompt = f"""
        Actúa como un experto turístico local. Necesito que generes {cantidad} puntos de interés turísticos reales y variados asociables a la ciudad base de: {ciudad}.
        
        REGLAS ESTRICTAS DE ESTRUCTURA Y FORMATO:
        1. El campo 'ciudad' DEBE SER EXACTAMENTE Y SIN EXCEPCIÓN "{ciudad}" para TODOS los registros devueltos.
        2. Si el lugar es una escapada/day-trip fuera de la mancha urbana:
           - Marca 'es_escapada_fuera' = True.
           - Pon el nombre del pueblo, municipio o región en el campo 'zona'.
        3. NO incluyas ninguno de estos lugares que ya existen en la base de datos: {existentes}
        4. Asegúrate de proporcionar coordenadas geográficas (latitud y longitud) precisas y reales.
        5. Diversifica las categorías (cultura, gastronomía, naturaleza, café, etc.).
        """

        # 3. Llamar a Gemini
        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ListaLugares,
            temperature=0.3
        )

        respuesta = ai_client.models.generate_content(
            model="gemini-flash-lite-latest",
            contents=prompt,
            config=config
        )

        datos = json.loads(respuesta.text)
        nuevos_lugares = datos["lugares"]

        if nuevos_lugares:
            supabase.table("lugares_multidestino").upsert(nuevos_lugares, on_conflict="nombre").execute()
            return True
        return False
    except Exception as e:
        print(f"Error en autogenerar_y_poblar: {e}")
        return False