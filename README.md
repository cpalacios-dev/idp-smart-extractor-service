
# IDP Smart Extractor Service 🤖📄

Servicio de procesamiento inteligente de documentos (IDP) que utiliza **IA Generativa (Gemini)** para extraer datos estructurados desde archivos PDF no estructurados (Boletas, Facturas, Liquidaciones).

## 🚀 Descripción del Proyecto

Este servicio expone una API REST construida con **Flask** que recibe documentos PDF, extrae su contenido de texto y utiliza modelos de lenguaje de última generación para transformar información caótica en datos JSON listos para ser procesados por sistemas ERP o bases de datos.

## 🛠️ Stack Tecnológico

-   🐍**Lenguaje:** Python 3.12+ (Compatible con Python 3.14)    
-   🌐**Framework Web:** Flask    
-   📄**Procesamiento PDF:** PyPDF    
-   🧠**Motor de IA:** Google Gemini 1.5 Flash / 2.0 (vía REST API)    
-   ✅**Validación de Datos:** Pydantic
    

## 🧠 Desafíos Técnicos Superados (Nivel Senior)

-   🔗**Bypass de SDK:** Ante incompatibilidades de las librerías oficiales de Google con versiones Alpha de Python (3.14), se implementó una conexión directa mediante **peticiones HTTP (REST)**, eliminando dependencias de binarios de C++ (Protobuf).    
-   ⏱️**Patrón de Resiliencia (Retry Scope):** Implementación de reintentos automáticos con espera exponencial para manejar límites de cuota de la API (Error 429).    
-   **Manejo de Archivos en Windows:** Solución al error de acceso denegado (`WinError 32`) mediante el uso de nombres temporales únicos (UUID) y cierres seguros de flujos de memoria.
    

## 📦 Instalación y Configuración

1.  📂**Clonar el repositorio:**
        
    ```Bash
    git clone <tu-url-repo>
    cd idp-smart-extractor-service
    ```
    
2.  🔑**Configurar variables de entorno:** Crea o edita el archivo `overlays/dev/.env.yaml`:
        
    ```YAML
    GEMINI_API_KEY: "TU_API_KEY_AQUI"
    ```
    
3.  ⚙️**Instalar dependencias:**
        
    ```Bash
    python -m pip install -r requirements.txt
    ```
    

## 🖥️ Uso del Servicio

1.  ▶️**Iniciar el servidor:**
    
    ```Bash
    python -m app.app
    ```
    _El servicio correrá en `http://127.0.0.1:8081`_
    
2.  🧪**Procesar un documento (Ejemplo con cURL):**
    
    ```Bash
    curl -X POST -F "file=@ruta/a/tu/boleta.pdf" http://127.0.0.1:8081/process-pdf
    ```
    

## 🐳 Dockerización

El proyecto incluye un `Dockerfile` optimizado basado en `python:3.12-slim`:

```Docker
# 🏗️ Construir la imagen
docker build -t idp-extractor .

# ▶️ Correr el contenedor
docker run -p 8081:8081 idp-extractor
```

## 📂 Estructura del Proyecto

```Plaintext
idp-smart-extractor-service/
├── app/
│   ├── core/           # 🧠 Lógica principal y esquemas Pydantic
│   ├── helpers/        # 🛠️ Utilidades de PDF e IA (REST API)
│   ├── data/           # 💾 Carpetas temporales de input/output
│   └── app.py          # 🌐 Punto de entrada Flask
├── overlays/           # ⚙️ Configuración por entorno (dev/qa/prod)
├── test_api.py         # 🧪 Script de pruebas unitarias
└── Dockerfile          # 🐳 Configuración de contenedor
```

----------

Desarrollado por **Cristian Palacios** - Ingeniero en Informática.