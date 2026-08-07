import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# Lista de lugares para enriquecer la base de datos
nuevos_lugares = [
    # --- Centro Histórico ---
    {
        "nombre": "Palacio de Bellas Artes",
        "categoria": "Museos y Arte",
        "zona": "Centro Histórico",
        "latitud": 19.4352,
        "longitud": -99.1412,
        "descripcion_corta": "Icono arquitectónico de la ciudad con murales de Rivera, Orozco y Siqueiros.",
        "costo_estimado": "Económico",
        "perfil_recomendado": "Familia, Pareja, Solo"
    },
    {
        "nombre": "Café Tacuba",
        "categoria": "Gastronomía Tradicional",
        "zona": "Centro Histórico",
        "latitud": 19.4358,
        "longitud": -99.1388,
        "descripcion_corta": "Restaurante clásico fundado en 1912 con comida tradicional mexicana y arquitectura colonial.",
        "costo_estimado": "Moderado",
        "perfil_recomendado": "Familia, Pareja"
    },
    {
        "nombre": "Templo Mayor",
        "categoria": "Museos y Arte",
        "zona": "Centro Histórico",
        "latitud": 19.4348,
        "longitud": -99.1317,
        "descripcion_corta": "Sitio arqueológico mexica y museo en el corazón del centro de la ciudad.",
        "costo_estimado": "Económico",
        "perfil_recomendado": "Familia, Solo, Amigos"
    },

    # --- Roma y Condesa ---
    {
        "nombre": "Café de Nadie",
        "categoria": "Café de especialidad",
        "zona": "Roma Norte",
        "latitud": 19.4182,
        "longitud": -99.1585,
        "descripcion_corta": "Cafetería y bar escudado en sistemas de alta fidelidad de sonido y café de origen.",
        "costo_estimado": "Moderado",
        "perfil_recomendado": "Pareja, Amigos, Solo"
    },
    {
        "nombre": "Parque México",
        "categoria": "Hiking y Naturaleza",
        "zona": "Condesa",
        "latitud": 19.4124,
        "longitud": -99.1691,
        "descripcion_corta": "Parque estilo Art Déco ideal para caminar, relajarse o pasear mascotas.",
        "costo_estimado": "Gratis",
        "perfil_recomendado": "Familia, Pareja, Solo"
    },
    {
        "nombre": "Contramar",
        "categoria": "Gastronomía Tradicional",
        "zona": "Roma Norte",
        "latitud": 19.4194,
        "longitud": -99.1673,
        "descripcion_corta": "Famoso restaurante de mariscos estilo costa del Pacífico, célebre por su pescado a la talla.",
        "costo_estimado": "Alto",
        "perfil_recomendado": "Pareja, Amigos, Lujo"
    },

    # --- Coyoacán y Sur ---
    {
        "nombre": "Museo Frida Kahlo (Casa Azul)",
        "categoria": "Museos y Arte",
        "zona": "Coyoacán",
        "latitud": 19.3551,
        "longitud": -99.1625,
        "descripcion_corta": "La histórica casa donde nació y murió la artista Frida Kahlo.",
        "costo_estimado": "Moderado",
        "perfil_recomendado": "Pareja, Solo, Amigos"
    },
    {
        "nombre": "Mercado de Coyoacán",
        "categoria": "Gastronomía Tradicional",
        "zona": "Coyoacán",
        "latitud": 19.3512,
        "longitud": -99.1610,
        "descripcion_corta": "Mercado folclórico famoso por sus tostadas, aguas frescas y artesanías.",
        "costo_estimado": "Económico",
        "perfil_recomendado": "Familia, Amigos, Solo"
    },

    # --- Polanco y Bosque de Chapultepec ---
    {
        "nombre": "Castillo de Chapultepec",
        "categoria": "Museos y Arte",
        "zona": "Polanco / Chapultepec",
        "latitud": 19.4204,
        "longitud": -99.1818,
        "descripcion_corta": "Único castillo real en América, alberga el Museo Nacional de Historia con vistas a la ciudad.",
        "costo_estimado": "Económico",
        "perfil_recomendado": "Familia, Pareja, Solo"
    },
    {
        "nombre": "Pujol",
        "categoria": "Lujo y Gourmet",
        "zona": "Polanco",
        "latitud": 19.4293,
        "longitud": -99.1963,
        "descripcion_corta": "Restaurante de alta cocina mexicana por el chef Enrique Olvera, famoso por su Mole Madre.",
        "costo_estimado": "Alto",
        "perfil_recomendado": "Pareja, Lujo"
    },
    {
        "nombre": "Museo Anahuacalli",
        "categoria": "Museos y Arte",
        "zona": "Coyoacán Sur",
        "latitud": 19.3236,
        "longitud": -99.1432,
        "descripcion_corta": "Diseñado por Diego Rivera en piedra volcánica para albergar su colección precolombina.",
        "costo_estimado": "Económico",
        "perfil_recomendado": "Solo, Pareja"
    }
]

def cargar_lugares():
    print("Iniciando la inserción de datos en Supabase...")
    
    try:
        respuesta = supabase.table("lugares_cdmx").upsert(nuevos_lugares, on_conflict="nombre").execute()
        print(f"✅ ¡Éxito! Se insertaron/actualizaron {len(respuesta.data)} lugares en la base de datos.")
    except Exception as e:
        print(f"❌ Error al insertar datos: {e}")

if __name__ == "__main__":
    cargar_lugares()