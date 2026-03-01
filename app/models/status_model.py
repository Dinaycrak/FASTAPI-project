from pydantic import BaseModel
from typing import Optional


class Status(BaseModel):
    id_estado: Optional[int] = None
    nombre_estado: str
    descripcion: str
