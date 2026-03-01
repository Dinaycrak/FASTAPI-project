from pydantic import BaseModel
from typing import Optional


class ProjectRol(BaseModel):
    id_rol_proyecto: Optional[int] = None
    nombre_rol: str
    descripcion: str
