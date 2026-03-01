from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Document(BaseModel):
    id_documento: Optional[int] = None
    id_proyecto: Optional[int] = None
    id_usuario: Optional[int] = None
    id_tipo_documento: Optional[int] = None
    nombre_archivo: str
    ruta_archivo: str
    descripcion: str
    fecha_subida: datetime
