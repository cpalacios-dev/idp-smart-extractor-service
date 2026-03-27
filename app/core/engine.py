"""
Motor principal de procesamiento (Orquestador).
"""
import logging
from app.helpers.pdf_helper import extraer_texto_local
from app.helpers.ai_handler import AIService

# Configuración de logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("IDP_ENGINE")

class IDPEngine:
    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service

    def procesar_documento(self, ruta_pdf: str) -> dict:
        """
        Orquesta el flujo completo de extracción: PDF -> Texto -> IA (JSON)
        """
        logger.info(f"⚙️ Motor IDP iniciando procesamiento de documento...")
        
        # 1. Extraer texto plano
        texto = extraer_texto_local(ruta_pdf)
        
        if texto == "ERROR_DOCUMENTO_ESCANEADO":
            raise ValueError("DOCUMENTO_ESCANEADO")
            
        # 2. Procesar con Inteligencia Artificial
        datos_estructurados = self.ai_service.extraer_datos_pdf(texto)
        
        logger.info("✅ Procesamiento completado con éxito.")
        return datos_estructurados