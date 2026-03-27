"""
Modelos de datos para validación de entrada/salida.
"""
from pydantic import BaseModel, Field
from typing import Optional

class DocumentoExtraido(BaseModel):
    nombre_empresa: str = Field(description="Nombre de la empresa que emite el documento")
    rut_emisor: str = Field(description="RUT de la empresa emisora")
    fecha_emision: str = Field(description="Fecha de emisión del documento")
    monto_total: Optional[float] = Field(description="Monto total a pagar o recibir, si aplica. Solo el número.", default=None)
    tipo_documento: str = Field(description="Ej: Factura Electrónica, Liquidación de Sueldo, Boleta de Honorarios, etc.")