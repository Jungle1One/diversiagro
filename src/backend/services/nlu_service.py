import os
import json
from dotenv import load_dotenv

load_dotenv()

try:
    import google.generativeai as genai
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
except ImportError:
    pass

def extract_municipio_and_coords(speech_result: str):
    if not os.getenv("GEMINI_API_KEY"):
        return None, None, None, None
        
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""
        Analiza este texto dicho por un campesino: "{speech_result}".
        Identifica el municipio y la zona rural (vereda/corregimiento) en el Valle del Cauca, Colombia.
        
        Responde ÚNICAMENTE un JSON válido con esta estructura exacta (no uses los ejemplos textualmente, extrae la información real del texto):
        {{
            "municipio": "<nombre_del_municipio_o_null>",
            "zona_rural": "<nombre_de_vereda_o_null>",
            "lat": <latitud_float_aproximada>,
            "lon": <longitud_float_aproximada>
        }}
        Asegúrate de estimar las coordenadas lat y lon reales de esa vereda/municipio en Colombia.
        """
        ai_res = model.generate_content(prompt)
        texto_limpio = ai_res.text.replace("```json", "").replace("```", "").strip()
        data = json.loads(texto_limpio)
        
        return data.get("municipio"), data.get("zona_rural"), data.get("lat"), data.get("lon")
    except Exception as e:
        print(f"Error Gemini: {e}")
        return None, None, None, None
