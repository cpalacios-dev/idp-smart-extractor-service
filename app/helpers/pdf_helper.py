"""
Helper para la lectura y extracción de texto desde archivos PDF (Pure Python).
"""
import logging
from pathlib import Path
from pypdf import PdfReader

# Configuración básica de log para el helper
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("PDF_HELPER")

def extraer_texto_local(ruta_pdf: str | Path) -> str:
    """
    Abre un archivo PDF y extrae todo su texto plano usando pypdf.
    """
    texto_completo = ""
    
    try:
        # EL FIX: Abrir el documento de forma segura para que Windows lo suelte al terminar
        with open(ruta_pdf, "rb") as archivo_pdf:
            reader = PdfReader(archivo_pdf)
            logger.info(f"📄 Procesando PDF: {Path(ruta_pdf).name} ({len(reader.pages)} páginas)")
            
            # Iterar sobre cada página y extraer el texto
            for pagina in reader.pages:
                texto_pagina = pagina.extract_text()
                if texto_pagina:
                    texto_completo += texto_pagina + "\n"
            
        # Validación de documentos escaneados (imágenes puras)
        if not texto_completo.strip():
            logger.warning("⚠️ El PDF parece ser un escaneo (sin texto digital). Se requiere OCR.")
            return "ERROR_DOCUMENTO_ESCANEADO"
            
        logger.info("✅ Texto extraído exitosamente.")
        return texto_completo.strip()
        
    except Exception as e:
        logger.error(f"❌ Error al intentar leer el PDF: {e}")
        raise Exception(f"Fallo en lectura de PDF: {e}")