import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

nuevos_lugares = [
    # ==========================================
    # --- CIUDAD DE MÉXICO ---
    # ==========================================
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

    # ==========================================
    # --- MÉRIDA ---
    # ==========================================
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
    {
        "nombre": "Gran Museo del Mundo Maya",
        "ciudad": "Mérida",
        "categoria": "Museos y Arte",
        "zona": "Norte / Cordemex",
        "es_escapada_fuera": False,
        "latitud": 21.0360,
        "longitud": -89.6293,
        "descripcion_corta": "Exposición moderna e interactiva sobre la historia y cultura maya.",
        "costo_estimado": "Moderado",
        "perfil_recomendado": "Familia, Solo, Amigos"
    },
    {
        "nombre": "Parque Santa Lucía",
        "ciudad": "Mérida",
        "categoria": "Gastronomía Tradicional",
        "zona": "Centro Histórico",
        "es_escapada_fuera": False,
        "latitud": 20.9706,
        "longitud": -89.6226,
        "descripcion_corta": "Plaza icónica con terrazas de restaurantes y serenatas yucatecas los jueves.",
        "costo_estimado": "Moderado",
        "perfil_recomendado": "Pareja, Familia, Amigos"
    },
    {
        "nombre": "Manifesto Specialty Coffee",
        "ciudad": "Mérida",
        "categoria": "Café de especialidad",
        "zona": "Centro Histórico",
        "es_escapada_fuera": False,
        "latitud": 20.9731,
        "longitud": -89.6221,
        "descripcion_corta": "Cafetería de especialidad con tostado artesanal en una casona colonial.",
        "costo_estimado": "Económico",
        "perfil_recomendado": "Solo, Pareja"
    },
    {
        "nombre": "Reserva Ecológica Cuxtal",
        "ciudad": "Mérida",
        "categoria": "Hiking y Naturaleza",
        "zona": "Sur / Periferia",
        "es_escapada_fuera": False,
        "latitud": 20.8521,
        "longitud": -89.6105,
        "descripcion_corta": "Área natural protegida ideal para observación de aves y caminatas tranquilas.",
        "costo_estimado": "Gratis",
        "perfil_recomendado": "Familia, Solo"
    },
    {
        "nombre": "Zona Arqueológica Uxmal",
        "ciudad": "Mérida",
        "categoria": "Excursión / Day-Trip",
        "zona": "Ruta Puuc",
        "es_escapada_fuera": True,
        "latitud": 20.3607,
        "longitud": -89.7713,
        "descripcion_corta": "Majestuosa ciudad maya famosa por la Pirámide del Adivino a 1h 15m de Mérida.",
        "costo_estimado": "Alto",
        "perfil_recomendado": "Familia, Pareja, Solo"
    },
    {
        "nombre": "Pueblo Mágico de Izamal",
        "ciudad": "Mérida",
        "categoria": "Excursión / Day-Trip",
        "zona": "Izamal",
        "es_escapada_fuera": True,
        "latitud": 20.9351,
        "longitud": -89.0182,
        "descripcion_corta": "La ciudad amarilla, conocida por su convento colonial e impresionantes pirámides.",
        "costo_estimado": "Económico",
        "perfil_recomendado": "Familia, Pareja, Solo"
    },

    # ==========================================
    # --- BARCELONA ---
    # ==========================================
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
    {
        "nombre": "Park Güell",
        "ciudad": "Barcelona",
        "categoria": "Hiking y Naturaleza",
        "zona": "Gràcia / Carmel",
        "es_escapada_fuera": False,
        "latitud": 41.4145,
        "longitud": 2.1527,
        "descripcion_corta": "Parque público con icónicos mosaicos y vistas panorámicas de Barcelona.",
        "costo_estimado": "Moderado",
        "perfil_recomendado": "Familia, Pareja, Solo"
    },
    {
        "nombre": "Barri Gòtic",
        "ciudad": "Barcelona",
        "categoria": "Museos y Arte",
        "zona": "Ciutat Vella",
        "es_escapada_fuera": False,
        "latitud": 41.3825,
        "longitud": 2.1769,
        "descripcion_corta": "Calles medievales estrechas, la Catedral de Barcelona y plazas históricas.",
        "costo_estimado": "Gratis",
        "perfil_recomendado": "Familia, Pareja, Solo, Amigos"
    },
    {
        "nombre": "Satan's Coffee Corner",
        "ciudad": "Barcelona",
        "categoria": "Café de especialidad",
        "zona": "Gótico",
        "es_escapada_fuera": False,
        "latitud": 41.3831,
        "longitud": 2.1772,
        "descripcion_corta": "Pioneros del café de especialidad con un ambiente urbano y vanguardista.",
        "costo_estimado": "Económico",
        "perfil_recomendado": "Solo, Amigos"
    },
    {
        "nombre": "El Xampanyet",
        "ciudad": "Barcelona",
        "categoria": "Gastronomía Tradicional",
        "zona": "El Born",
        "es_escapada_fuera": False,
        "latitud": 41.3848,
        "longitud": 2.1812,
        "descripcion_corta": "Taverna tradicional famosa por su cava de la casa, anchoas y tapas auténticas.",
        "costo_estimado": "Moderado",
        "perfil_recomendado": "Amigos, Pareja"
    },
    {
        "nombre": "Pueblo Costero de Sitges",
        "ciudad": "Barcelona",
        "categoria": "Excursión / Day-Trip",
        "zona": "Costa del Garraf",
        "es_escapada_fuera": True,
        "latitud": 41.2372,
        "longitud": 1.8059,
        "descripcion_corta": "Hermosa villa marinera con playas, paseo marítimo y arte a 40 min en tren.",
        "costo_estimado": "Moderado",
        "perfil_recomendado": "Familia, Pareja, Amigos"
    },
    {
        "nombre": "Girona Histórica",
        "ciudad": "Barcelona",
        "categoria": "Excursión / Day-Trip",
        "zona": "Girona",
        "es_escapada_fuera": True,
        "latitud": 41.9831,
        "longitud": 2.8249,
        "descripcion_corta": "Ciudad medieval con un barrio judío conservado y murallas a 38 min en tren de alta velocidad.",
        "costo_estimado": "Moderado",
        "perfil_recomendado": "Familia, Pareja, Solo"
    },

    # ==========================================
    # --- CUSCO ---
    # ==========================================
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
    },
    {
        "nombre": "Barrio de San Blas",
        "ciudad": "Cusco",
        "categoria": "Museos y Arte",
        "zona": "San Blas",
        "es_escapada_fuera": False,
        "latitud": -13.5156,
        "longitud": -71.9742,
        "descripcion_corta": "Barrio bohemio con talleres de artesanos, galerías y miradores hacia la ciudad.",
        "costo_estimado": "Gratis",
        "perfil_recomendado": "Pareja, Solo, Amigos"
    },
    {
        "nombre": "Mercado Central de San Pedro",
        "ciudad": "Cusco",
        "categoria": "Mercados Locales",
        "zona": "Centro Histórico",
        "es_escapada_fuera": False,
        "latitud": -13.5207,
        "longitud": -71.9822,
        "descripcion_corta": "El mercado más vivo de Cusco para probar jugos frescos, sopas y comprar artesanías.",
        "costo_estimado": "Económico",
        "perfil_recomendado": "Familia, Amigos, Solo"
    },
    {
        "nombre": "Three Monkeys Coffee Bar",
        "ciudad": "Cusco",
        "categoria": "Café de especialidad",
        "zona": "Centro Histórico",
        "es_escapada_fuera": False,
        "latitud": -13.5178,
        "longitud": -71.9765,
        "descripcion_corta": "Café de especialidad con granos de origen peruano de la cuenca amazónica cusqueña.",
        "costo_estimado": "Económico",
        "perfil_recomendado": "Solo, Pareja"
    },
    {
        "nombre": "Cicciolina",
        "ciudad": "Cusco",
        "categoria": "Lujo y Gourmet",
        "zona": "Centro Histórico",
        "es_escapada_fuera": False,
        "latitud": -13.5161,
        "longitud": -71.9754,
        "descripcion_corta": "Restaurante y tapas bar en un segundo piso colonial con cocina mediterránea-andina.",
        "costo_estimado": "Alto",
        "perfil_recomendado": "Pareja, Amigos"
    },
    {
        "nombre": "Salineras de Maras y Terrazas de Moray",
        "ciudad": "Cusco",
        "categoria": "Excursión / Day-Trip",
        "zona": "Valle Sagrado",
        "es_escapada_fuera": True,
        "latitud": -13.3321,
        "longitud": -72.1585,
        "descripcion_corta": "Miles de pozos artesanales de sal y el laboratorio agrícola inca en Moray.",
        "costo_estimado": "Moderado",
        "perfil_recomendado": "Familia, Pareja, Amigos"
    },
    {
        "nombre": "Montaña de Siete Colores (Vinicunca)",
        "ciudad": "Cusco",
        "categoria": "Excursión / Day-Trip",
        "zona": "Canchis",
        "es_escapada_fuera": True,
        "latitud": -13.8694,
        "longitud": -71.3030,
        "descripcion_corta": "Impresionante paisaje natural a más de 5,000 msnm para caminata exigente.",
        "costo_estimado": "Moderado",
        "perfil_recomendado": "Amigos, Solo"
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