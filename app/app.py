import os
import sys
import uuid
from pathlib import Path

os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

# Agregar el directorio raíz al path para que Python reconozca la carpeta 'app' como paquete
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

import yaml
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from app.helpers.ai_handler import AIService
from app.core.engine import IDPEngine

app = Flask(__name__)

# 1. Cargar config
overlay_path = Path(__file__).resolve().parent.parent / "overlays" / "dev" / ".env.yaml"
try:
    with open(overlay_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
        api_key = config.get("GEMINI_API_KEY")
except FileNotFoundError:
    raise RuntimeError(f"⚠️ No se encontró el archivo de configuración en: {overlay_path}")

# 2. Inicializar Servicios y el Motor (Engine)
ai_service = AIService(api_key=api_key)
engine = IDPEngine(ai_service=ai_service)

# 3. Configurar la carpeta temporal
UPLOAD_FOLDER = Path(__file__).resolve().parent / "data" / "input"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

@app.route('/process-pdf', methods=['POST'])
def process_pdf():
    # Validaciones iniciales
    if 'file' not in request.files:
        return jsonify({"error": "No se envió ningún archivo"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "El archivo no tiene nombre"}), 400
        
    # FIX: Generamos un nombre único temporal para evitar choques de archivos
    filename = secure_filename(file.filename)
    nombre_unico = f"temp_{uuid.uuid4().hex[:8]}_{filename}"
    temp_path = UPLOAD_FOLDER / nombre_unico
    
    file.save(temp_path)
    
    try:
        # DELEGAMOS TODO AL MOTOR
        datos_estructurados = engine.procesar_documento(str(temp_path))
        
        return jsonify({
            "status": "success",
            "data": datos_estructurados
        }), 200
        
    except ValueError as ve:
        if str(ve) == "DOCUMENTO_ESCANEADO":
            return jsonify({"status": "error", "message": "El documento es un escaneo. Requiere OCR."}), 422
        return jsonify({"status": "error", "message": str(ve)}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
        
    finally:
        # Limpieza de seguridad
        if temp_path.exists():
            os.remove(temp_path)

if __name__ == '__main__':
    app.run(port=8081, debug=True)