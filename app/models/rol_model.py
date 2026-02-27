from pydantic import BaseModel
from typing import Optional


class Rol(BaseModel):
    id_rol: Optional[int] = None
    nombre_rol: str
    descripcion: str
