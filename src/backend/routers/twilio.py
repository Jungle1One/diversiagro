from fastapi import APIRouter, Form
from fastapi.responses import Response
import urllib.parse
import requests as req_http

from src.backend.services.nlu_service import extract_municipio_and_coords
from src.backend.services.gis_service import get_municipio_centroid, normalize_text, gdf_municipios
from src.backend.schemas import PredictCoordsRequest
from src.backend.services.ml_service import run_model_pipeline
from src.backend.services.gis_service import get_gis_features

try:
    from twilio.twiml.voice_response import VoiceResponse
except ImportError:
    pass

router = APIRouter()

@router.post("/voice")
async def twilio_voice(attempts: int = 0):
    response = VoiceResponse()
    
    if attempts >= 3:
        response.say("Ha superado el número de intentos permitidos. Gracias por comunicarse con DiversiAgro. Hasta pronto.", language='es-MX', voice='alice')
        response.hangup()
        return Response(content=str(response), media_type="application/xml")
        
    gather = response.gather(
        input='speech',
        action=f'/twilio/process_speech_redirect?attempts={attempts}',
        timeout=5,
        language='es-CO',
        speechTimeout='auto'
    )
    gather.say(
        "Bienvenido a DiversIAgro. Diga su municipio y vereda.",
        language='es-MX', voice='alice'
    )
    response.redirect(f'/twilio/voice?attempts={attempts + 1}')
    return Response(content=str(response), media_type="application/xml")

@router.post("/process_speech_redirect")
async def twilio_process_speech_redirect(attempts: int = 0, SpeechResult: str = Form(default="")):
    response = VoiceResponse()
    if not SpeechResult:
        response.say("No escuché. Repita.", language='es-MX', voice='alice')
        response.redirect(f'/twilio/voice?attempts={attempts + 1}')
        return Response(content=str(response), media_type="application/xml")
        
    response.say("Buscando su ubicación...", language='es-MX', voice='alice')
    safe_speech = urllib.parse.quote(SpeechResult)
    response.redirect(f'/twilio/process_municipio?speech={safe_speech}&attempts={attempts}')
    return Response(content=str(response), media_type="application/xml")

@router.post("/process_municipio")
async def twilio_process_municipio(speech: str = "", attempts: int = 0):
    response = VoiceResponse()
    SpeechResult = urllib.parse.unquote(speech)
    
    muni, zona_rural, lat, lon = extract_municipio_and_coords(SpeechResult)
    
    if not muni:
        texto_norm = normalize_text(SpeechResult).lower()
        if gdf_municipios is not None and 'MPIO_NORM' in gdf_municipios.columns:
            for m in gdf_municipios['MPIO_NORM'].unique():
                if str(m).lower() in texto_norm:
                    muni = str(m).title()
                    break

    if not muni:
        response.say("Lo siento, no reconocí el municipio.", language='es-MX', voice='alice')
        response.redirect(f'/twilio/voice?attempts={attempts + 1}')
        return Response(content=str(response), media_type="application/xml")

    if lat is None or lon is None:
        centro = await get_municipio_centroid(muni)
        lat = centro["lat"]
        lon = centro["lon"]

    lugar_voz = f"{zona_rural}, {muni}" if zona_rural else f"{muni}"

    gather = response.gather(
        numDigits=1,
        action=f'/twilio/menu_action?municipio={muni}&lat={lat}&lon={lon}&attempts=0',
        timeout=7
    )
    gather.say(
        f"{lugar_voz}. Marque 1 para Clima. 2 para Alternativas de cultivo. 3 para Salir.",
        language='es-MX', voice='alice'
    )
    response.redirect(f'/twilio/menu_repeat?municipio={muni}&lat={lat}&lon={lon}&attempts=1')
    return Response(content=str(response), media_type="application/xml")

@router.post("/menu_repeat")
async def twilio_menu_repeat(municipio: str, lat: float, lon: float, attempts: int = 0):
    response = VoiceResponse()
    
    if attempts >= 3:
        response.say("Ha superado el número de intentos permitidos. Gracias por comunicarse con DiversiAgro. Hasta pronto.", language='es-MX', voice='alice')
        response.hangup()
        return Response(content=str(response), media_type="application/xml")
        
    gather = response.gather(
        numDigits=1,
        action=f'/twilio/menu_action?municipio={municipio}&lat={lat}&lon={lon}&attempts={attempts}',
        timeout=7
    )
    gather.say(
        "Marque 1 para Clima. 2 para Alternativas. 3 para Salir.",
        language='es-MX', voice='alice'
    )
    response.redirect(f'/twilio/menu_repeat?municipio={municipio}&lat={lat}&lon={lon}&attempts={attempts + 1}')
    return Response(content=str(response), media_type="application/xml")

@router.post("/menu_action")
async def twilio_menu_action(municipio: str, lat: float, lon: float, attempts: int = 0, Digits: str = Form(default="")):
    response = VoiceResponse()
    
    if Digits == "1":
        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            res = req_http.get(url, timeout=10).json()
            temp = res['current_weather']['temperature']
            viento = res['current_weather']['windspeed']
            response.say(f"Temperatura: {temp} grados. Viento: {viento} kilómetros por hora.", language='es-MX', voice='alice')
            
            response.pause(length=1)
            response.say("Gracias por comunicarte con DiversiAgro. Hasta pronto.", language='es-MX', voice='alice')
            response.hangup()
        except Exception:
            response.say("Error al consultar el clima.", language='es-MX', voice='alice')
            response.redirect(f'/twilio/menu_repeat?municipio={municipio}&lat={lat}&lon={lon}&attempts={attempts + 1}')
            
    elif Digits == "2":
        try:
            _, altitud, pendiente, lluvia = get_gis_features(lat, lon)
            
            # Para evitar el timeout de 15 segundos de Twilio, desactivamos Kriging.
            _, _, score_aguacate, apt_aguacate = run_model_pipeline("aguacate", lat, lon, altitud, pendiente, lluvia, use_kriging=False)
            _, _, score_cacao, apt_cacao = run_model_pipeline("cacao", lat, lon, altitud, pendiente, lluvia, use_kriging=False)
            _, _, score_fresa, apt_fresa = run_model_pipeline("fresa", lat, lon, altitud, pendiente, lluvia, use_kriging=False)
            
            recomendado_apt = {
                "aguacate": score_aguacate,
                "cacao": score_cacao,
                "fresa": score_fresa
            }
            recomendado = max(recomendado_apt, key=recomendado_apt.get)
            msg = f"Aptitud para aguacate: {apt_aguacate.lower()}. Aptitud para cacao: {apt_cacao.lower()}. Aptitud para fresa: {apt_fresa.lower()}. Recomendamos: {recomendado}."
            response.say(msg, language='es-MX', voice='alice')
            
            response.pause(length=1)
            response.say("Gracias por comunicarte con DiversiAgro. Hasta pronto.", language='es-MX', voice='alice')
            response.hangup()
        except Exception as e:
            import traceback
            traceback.print_exc()
            response.say("Error al evaluar cultivos.", language='es-MX', voice='alice')
            response.redirect(f'/twilio/menu_repeat?municipio={municipio}&lat={lat}&lon={lon}&attempts={attempts + 1}')
            
    elif Digits == "3":
        response.say("Gracias. Hasta pronto.", language='es-MX', voice='alice')
        response.hangup()
        
    else:
        response.say("Opción inválida.", language='es-MX', voice='alice')
        response.redirect(f'/twilio/menu_repeat?municipio={municipio}&lat={lat}&lon={lon}&attempts={attempts + 1}')

    return Response(content=str(response), media_type="application/xml")
