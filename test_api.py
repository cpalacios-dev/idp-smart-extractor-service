import requests
import json
import sys

# 1. Pon el nombre exacto de tu archivo aquí
NOMBRE_ARCHIVO = "Boleta_Luz.pdf"  # <--- ¡CAMBIA ESTO!
ruta_pdf = f"app/data/input/{NOMBRE_ARCHIVO}"

print(f"🚀 Enviando '{ruta_pdf}' a la API de Extracción Inteligente...")

url = "http://127.0.0.1:8081/process-pdf"

try:
    # 2. Abrimos el PDF y lo enviamos por POST
    with open(ruta_pdf, "rb") as archivo:
        archivos = {"file": archivo}
        respuesta = requests.post(url, files=archivos)
    
    # 3. Imprimimos el resultado
    if respuesta.status_code == 200:
        datos = respuesta.json()
        print("\n✅ ¡Extracción Exitosa! La IA devolvió esto:")
        print(json.dumps(datos, indent=4, ensure_ascii=False))
    else:
        print(f"\n❌ Error del servidor ({respuesta.status_code}): {respuesta.text}")

except FileNotFoundError:
    print(f"\n❌ ¡Alto ahí! No se encontró el archivo '{ruta_pdf}'.")
    print("Asegúrate de que el PDF esté dentro de la carpeta 'app/data/input/' y el nombre esté bien escrito.")
except requests.exceptions.ConnectionError:
    print("\n❌ Error de conexión: ¿Seguro que el servidor Flask está corriendo en otra terminal?")