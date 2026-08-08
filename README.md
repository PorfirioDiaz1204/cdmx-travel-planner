# 🗺️ CDMX Travel Planner (MVP)

> Un asistente de viajes inteligente que genera itinerarios personalizados por la Ciudad de México combinando IA generativa y datos geográficos.

![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?style=flat&logo=streamlit)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python)
![Supabase](https://img.shields.io/badge/Database-Supabase-3ECF8E?style=flat&logo=supabase)
![Google Gemini](https://img.shields.io/badge/AI-Google%20Gemini-8E75B2?style=flat&logo=google)

---

## 🌟 Características Principales

* **Itinerarios Dinámicos con IA:** Generación de rutas optimizadas día por día según el perfil de viaje y preferencias del usuario.
* **Base de Datos Vectorial/Relacional:** Integración con **Supabase** para consultar lugares reales, coordenadas y categorías en la CDMX.
* **Mapas Interactivos:** Visualización geoespacial de cada actividad del día mediante **Folium** e integración nativa con Streamlit.
* **Exportación Multiformato:** Descarga de itinerarios en formatos **PDF** estructurado y **TXT** plano para consulta sin conexión.

---

## 🛠️ Arquitectura y Tecnologías

* **Frontend:** [Streamlit](https://streamlit.io/) + [Streamlit-Folium](https://github.com/randyzwitch/streamlit-folium)
* **Backend & LLM:** Python, Pydantic (validación de esquemas JSON), `google-genai` (Gemini API)
* **Base de Datos:** [Supabase](https://supabase.com/) (PostgreSQL)
* **Generación de Documentos:** [ReportLab](https://www.reportlab.com/)

---

## 🚀 Instalación y Ejecución Local

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/TU_USUARIO/cdmx-travel-planner.git](https://github.com/TU_USUARIO/cdmx-travel-planner.git)
   cd cdmx-travel-planner