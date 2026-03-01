from pydantic import BaseModel
from typing import Optional


class DeliveryStatus(BaseModel):
    id_estado_entrega: Optional[int] = None
    nombre_estado: str
    descripcion: str
