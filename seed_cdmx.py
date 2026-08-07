import os
import json
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import List

# 1. Cargar variables de entorno
load_dotenv()
load_dotenv("ROOT.env")
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("No se encontró GEMINI_API_KEY en los archivos .env o ROOT.env")

client = genai.Client(api_key=api_key)

# 2. Definir el esquema exacto de salida usando Pydantic
class LugarCDMX(BaseModel):
    nombre: str = Field(description="Nombre oficial del lugar o establecimiento")
    categoria: str = Field(description="Opciones: 'cafeteria', 'museo', 'galeria', 'hiking', 'restaurante', 'deportes'")
    zona: str = Field(description="Opciones: 'Roma-Condesa', 'Centro Histórico', 'Coyoacán', 'Polanco', 'San Ángel', 'Chapultepec'")
    costo_nivel: int = Field(description="Nivel de costo del 1 ($) al 4 ($$$$)")
    tags: List[str] = Field(description="Lista de etiquetas descriptivas ej. ['pet-friendly', 'al-aire-libre', 'familiar']")
    latitud: float = Field(description="Coordenada de latitud aproximada")
    longitud: float = Field(description="Coordenada de longitud aproximada")
    descripcion_corta: str = Field(description="Resumen de 1-2 oraciones sobre la vibra o atractivo del lugar")

class CatalogoLugares(BaseModel):
    lugares: List[LugarCDMX]

# 3. Configurar el modelo
config = types.GenerateContentConfig(
    response_mime_type="application/json",
    response_schema=CatalogoLugares,
    temperature=0.2,
)

# 3.1 Ajustes de ritmo para evitar saturar la API
REQUEST_DELAY_SECONDS = 32
MAX_RETRIES = 3

# 4. Prompt para generar el conjunto de datos inicial
prompt = """
Genera una lista de 30 lugares emblemáticos e imperdibles en la Ciudad de México para visitantes.
Asegúrate de incluir una mezcla equilibrada de:
- Cafeterías de especialidad (Roma/Condesa/Coyoacán)
- Museos y galerías
- Parques y rutas de senderismo/hiking cercanas (ej. Desierto de los Leones, Dinamos, Chapultepec)
- Lugares gastronómicos y culturales tradicionales.

Devuelve información fáctica y coordenadas geográficas reales.
"""

print("Generando catálogo inicial de lugares para CDMX...")

response = None
for attempt in range(1, MAX_RETRIES + 1):
    try:
        print(f"Intento {attempt} de {MAX_RETRIES}...")
        response = client.models.generate_content(
            model="gemini-flash-lite-latest",
            contents=prompt,
            config=config,
        )
        break
    except Exception as e:
        error_message = str(e)
        print(f"Intento {attempt} fallido: {error_message}")
        if attempt < MAX_RETRIES:
            print(f"Esperando {REQUEST_DELAY_SECONDS} segundos antes de reintentar...")
            time.sleep(REQUEST_DELAY_SECONDS)
        else:
            print("❌ Error al consultar Gemini después de varios intentos:")
            print(error_message)
            print("\nPosibles causas: cuota agotada, límite de requests o problema con la clave API.")
            raise SystemExit(1)

# 5. Guardar en un archivo JSON local
output_filename = "cdmx_places_seed.json"

try:
    text = response.text
    data = json.loads(text)
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"✅ ¡Éxito! Se han guardado {len(data.get('lugares', []))} lugares en '{output_filename}'.")
except Exception as e:
    print(f"❌ Error al procesar el JSON: {e}")
    print("Texto recibido:")
    print(text if 'text' in locals() else 'No se recibió texto')