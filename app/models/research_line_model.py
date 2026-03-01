from pydantic import BaseModel
from typing import Optional


class ResearchLine(BaseModel):
    id_linea: Optional[int] = None
    nombre_linea: str
    descripcion: str
