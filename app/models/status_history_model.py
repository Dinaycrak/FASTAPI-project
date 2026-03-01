from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class StatusHistory(BaseModel):
    id_historial: Optional[int] = None
    id_estado_anterior: Optional[int] = None
    id_estado_nuevo: Optional[int] = None
    cambiado_por: Optional[int] = None
    fecha_cambio: datetime 
