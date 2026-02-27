from pydantic import BaseModel
from typing import Optional


class DocumentType(BaseModel):
    id_tipo_documento: Optional[int] = None
    nombre_tipo: str
    descripcion: str