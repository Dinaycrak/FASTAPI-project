from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ScheduledDelivery(BaseModel):
    id_entrega: Optional[int] = None
    id_proyecto: Optional[int] = None
    fecha_limite: datetime 
    descripcion: str
    id_estado_entrega: str