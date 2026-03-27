"""
Helper para la integración con IA mediante REST API (Bypass SDK con Retry Automático).
"""
import requests
import json
import logging
import time
from app.core.schemas import DocumentoExtraido

# Configuración básica de log
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("AI_HANDLER_REST")

class AIService:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("No se proporcionó API Key para Gemini.")
        
        self.api_key = api_key
        # URL actualizada a Gemini 3 Flash
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={self.api_key}"

    def extraer_datos_pdf(self, texto_pdf: str) -> dict:
        logger.info("🤖 Iniciando análisis con IA (Gemini REST API)...")
        
        esquema_json = DocumentoExtraido.model_json_schema()
        
        prompt = f"""
        Eres un experto en extracción de datos de documentos financieros y legales chilenos.
        Analiza el siguiente texto extraído de un documento PDF.
        
        Tu única tarea es extraer los datos y responder EXCLUSIVAMENTE con un JSON válido 
        que respete esta estructura exacta:
        {json.dumps(esquema_json, indent=2)}
        
        No incluyas saludos, ni explicaciones. SOLO el JSON puro.
        Si un dato no existe, pon null.
        
        Texto del documento:
        {texto_pdf}
        """
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseMimeType": "application/json"}
        }
        headers = {'Content-Type': 'application/json'}
        
        # SISTEMA DE REINTENTOS (Retry Pattern)
        max_reintentos = 3
        for intento in range(max_reintentos):
            try:
                response = requests.post(self.url, json=payload, headers=headers)
                response.raise_for_status() # Lanza error si Google nos rechaza
                
                # Navegamos la respuesta JSON
                resultado_bruto = response.json()
                texto_ia = resultado_bruto['candidates'][0]['content']['parts'][0]['text']
                
                # Limpiamos y validamos
                datos_json = json.loads(texto_ia)
                datos_validados = DocumentoExtraido(**datos_json)
                
                logger.info("✅ Datos extraídos y validados correctamente por la IA.")
                return datos_validados.model_dump()
                
            except requests.exceptions.HTTPError as e:
                # Si es el error 429 (Too Many Requests), esperamos y reintentamos
                if response.status_code == 429:
                    tiempo_espera = 15 * (intento + 1) # Espera 15s, luego 30s...
                    logger.warning(f"⚠️ Límite de Google (429). El robot esperará {tiempo_espera} segundos... (Intento {intento+1}/{max_reintentos})")
                    time.sleep(tiempo_espera)
                    continue
                else:
                    logger.error(f"❌ Error HTTP {response.status_code}: {response.text}")
                    raise Exception(f"Rechazo de API: {response.status_code}")
                    
            except json.JSONDecodeError as e:
                logger.error(f"❌ La IA no devolvió un JSON válido: {e}")
                raise Exception("Error de formato en la respuesta de la IA.")
            except Exception as e:
                logger.error(f"❌ Error inesperado: {e}")
                raise
                
        # Si el loop termina y no logró conectarse
        raise Exception("Se agotaron los reintentos para comunicarse con la IA. Intenta más tarde.")