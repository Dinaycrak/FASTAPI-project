from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Progress(BaseModel):
    id_avance: Optional[int] = None
    id_proyecto: Optional[int] = None
    id_usuario: Optional[int] = None
    descripcion: str
    porcentaje_avance: str
    fecha_registro: datetime
