from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Project(BaseModel):
    id_proyecto: Optional[int] = None
    nombre_proyecto: str
    descripcion: str
    fecha_inicio: datetime
    fecha_fin: datetime
    id_estado: Optional[int] = None
    id_linea: Optional[int] = None
    creado_por: str
    fecha_creacion: datetime