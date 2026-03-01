from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserProject(BaseModel):
    id_proyecto_usuario: Optional[int] = None
    id_proyecto: Optional[int] = None
    id_usuario: Optional[int] = None
    id_rol_proyecto: Optional[int] = None
    fecha_asignacion: datetime
