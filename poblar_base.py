import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

nuevos_lugares = [
    # --- CIUDAD DE MÉXICO ---
    {
        "nombre": "Palacio de Bellas Artes",
        "ciudad": "Ciudad de México",
        "categoria": "Museos y Arte",
        "zona": "Centro Histórico",
        "es_escapada_fuera": False,
        "latitud": 19.4352,
        "longitud": -99.1412,
        "descripcion_corta": "Icono arquitectónico con murales de Rivera, Orozco y Siqueiros.",
        "costo_estimado": "Económico",
        "perfil_recomendado": "Familia, Pareja, Solo"
    },
    {
        "nombre": "Café Tacuba",
        "ciudad": "Ciudad de México",
        "categoria": "Gastronomía Tradicional",
        "zona": "Centro Histórico",
        "es_escapada_fuera": False,
        "latitud": 19.4358,
        "longitud": -99.1388,
        "descripcion_corta": "Restaurante clásico fundado en 1912 con comida tradicional mexicana.",
        "costo_estimado": "Moderado",
        "perfil_recomendado": "Familia, Pareja"
    },
    {
        "nombre": "Museo Frida Kahlo (Casa Azul)",
        "ciudad": "Ciudad de México",
        "categoria": "Museos y Arte",
        "zona": "Coyoacán",
        "es_escapada_fuera": False,
        "latitud": 19.3551,
        "longitud": -99.1625,
        "descripcion_corta": "La histórica casa donde nació y murió la artista Frida Kahlo.",
        "costo_estimado": "Moderado",
        "perfil_recomendado": "Pareja, Solo, Amigos"
    },
    {
        "nombre": "Teotihuacán",
        "ciudad": "Ciudad de México",
        "categoria": "Excursión / Day-Trip",
        "zona": "Periferia / Valle de Teotihuacán",
        "es_escapada_fuera": True,
        "latitud": 19.6925,
        "longitud": -98.8438,
        "descripcion_corta": "Zona arqueológica monumental con las Pirámides del Sol y de la Luna a 1h de CDMX.",
        "costo_estimado": "Moderado",
        "perfil_recomendado": "Familia, Amigos, Solo"
    },

    # --- MÉRIDA (Ciudad Hub) ---
    {
        "nombre": "Paseo de Montejo",
        "ciudad": "Mérida",
        "categoria": "Hiking y Naturaleza",
        "zona": "Centro",
        "es_escapada_fuera": False,
        "latitud": 20.9883,
        "longitud": -89.6186,
        "descripcion_corta": "Avenida principal con casonas afrancesadas de la época del henequén.",
        "costo_estimado": "Gratis",
        "perfil_recomendado": "Familia, Pareja, Solo"
    },
    {
        "nombre": "Mercado Lucas de Gálvez",
        "ciudad": "Mérida",
        "categoria": "Mercados Locales",
        "zona": "Centro Histórico",
        "es_escapada_fuera": False,
        "latitud": 20.9634,
        "longitud": -89.6201,
        "descripcion_corta": "Mercado tradicional para probar cochinita pibil, panuchos y marquesitas.",
        "costo_estimado": "Económico",
        "perfil_recomendado": "Familia, Amigos, Solo"
    },
    {
        "nombre": "Cenote Xbatún",
        "ciudad": "Mérida",
        "categoria": "Excursión / Day-Trip",
        "zona": "San Antonio Mulix",
        "es_escapada_fuera": True,
        "latitud": 20.6681,
        "longitud": -89.7694,
        "descripcion_corta": "Cenote abierto de aguas cristalinas rodeado de vegetación a 50 min de Mérida.",
        "costo_estimado": "Económico",
        "perfil_recomendado": "Familia, Pareja, Amigos"
    },
    {
        "nombre": "Chichén Itzá",
        "ciudad": "Mérida",
        "categoria": "Excursión / Day-Trip",
        "zona": "Pisté",
        "es_escapada_fuera": True,
        "latitud": 20.6843,
        "longitud": -88.5678,
        "descripcion_corta": "Maravilla del mundo moderno y centro ceremonial maya a 1.5h de la ciudad.",
        "costo_estimado": "Alto",
        "perfil_recomendado": "Familia, Pareja, Solo"
    },

    # --- BARCELONA ---
    {
        "nombre": "Basílica de la Sagrada Família",
        "ciudad": "Barcelona",
        "categoria": "Museos y Arte",
        "zona": "Eixample",
        "es_escapada_fuera": False,
        "latitud": 41.4036,
        "longitud": 2.1744,
        "descripcion_corta": "La obra maestra de Antoni Gaudí y el monumento más icónico de Barcelona.",
        "costo_estimado": "Moderado",
        "perfil_recomendado": "Familia, Pareja, Solo"
    },
    {
        "nombre": "Mercat de la Boqueria",
        "ciudad": "Barcelona",
        "categoria": "Mercados Locales",
        "zona": "Ciutat Vella / La Rambla",
        "es_escapada_fuera": False,
        "latitud": 41.3817,
        "longitud": 2.1715,
        "descripcion_corta": "Mercado gastronómico lleno de tapas, mariscos frescos y frutas.",
        "costo_estimado": "Moderado",
        "perfil_recomendado": "Familia, Amigos, Solo"
    },
    {
        "nombre": "Monasterio de Montserrat",
        "ciudad": "Barcelona",
        "categoria": "Excursión / Day-Trip",
        "zona": "Monistrol de Montserrat",
        "es_escapada_fuera": True,
        "latitud": 41.5933,
        "longitud": 1.8375,
        "descripcion_corta": "Santuario enclavado en peculiares montañas rocosas a 1h en tren de Barcelona.",
        "costo_estimado": "Moderado",
        "perfil_recomendado": "Familia, Pareja, Solo"
    },

    # --- CUSCO (Ciudad Hub) ---
    {
        "nombre": "Plaza de Armas de Cusco",
        "ciudad": "Cusco",
        "categoria": "Gastronomía Tradicional",
        "zona": "Centro Histórico",
        "es_escapada_fuera": False,
        "latitud": -13.5167,
        "longitud": -71.9781,
        "descripcion_corta": "Corazón de la ciudad imperial inca con arquitectura colonial y cafés.",
        "costo_estimado": "Gratis",
        "perfil_recomendado": "Familia, Pareja, Solo"
    },
    {
        "nombre": "Sacsayhuamán",
        "ciudad": "Cusco",
        "categoria": "Museos y Arte",
        "zona": "Periferia Norte",
        "es_escapada_fuera": False,
        "latitud": -13.5078,
        "longitud": -71.9817,
        "descripcion_corta": "Fortaleza ceremonial inca famosa por sus enormes bloques de piedra tallados.",
        "costo_estimado": "Moderado",
        "perfil_recomendado": "Familia, Amigos, Solo"
    },
    {
        "nombre": "Ollantaytambo (Valle Sagrado)",
        "ciudad": "Cusco",
        "categoria": "Excursión / Day-Trip",
        "zona": "Valle Sagrado",
        "es_escapada_fuera": True,
        "latitud": -13.2583,
        "longitud": -72.2633,
        "descripcion_corta": "Pueblo e imponente recinto arqueológico inca a 1.5h de Cusco.",
        "costo_estimado": "Moderado",
        "perfil_recomendado": "Familia, Pareja, Amigos"
    }
]

def cargar_lugares():
    print("Iniciando la inserción de datos multidestino en Supabase...")
    try:
        respuesta = supabase.table("lugares_multidestino").upsert(nuevos_lugares, on_conflict="nombre").execute()
        print(f"✅ ¡Éxito! Se insertaron/actualizaron {len(respuesta.data)} lugares.")
    except Exception as e:
        print(f"❌ Error al insertar datos: {e}")

if __name__ == "__main__":
    cargar_lugares()