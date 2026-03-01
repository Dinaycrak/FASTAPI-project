from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Comments(BaseModel):
    id_comentario: Optional[int] = None
    id_avance: Optional[int] = None
    id_usuario: Optional[int] = None
    contenido: str
    fecha_comentario: datetime