import os
import json
from dotenv import load_dotenv
from supabase import create_client, Client

# 1. Cargar variables
load_dotenv()
load_dotenv("ROOT.env")

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    raise ValueError("Faltan las credenciales de SUPABASE_URL o SUPABASE_KEY en el .env")

supabase: Client = create_client(url, key)

# 2. Cargar JSON local
with open("cdmx_places_seed.json", "r", encoding="utf-8") as f:
    data = json.load(f)

lugares = data.get("lugares", [])

print(f"Subiendo {len(lugares)} lugares a Supabase...")

# 3. Insertar registros
try:
    response = supabase.table("lugares_cdmx").insert(lugares).execute()
    print("✅ ¡Éxito! Datos cargados correctamente a la nube.")
except Exception as e:
    print(f"❌ Error al subir a Supabase: {e}")