from pydantic import BaseModel

class DocumentType(BaseModel):
    id: int = None
    nombre_tipo: str
    descripcion: str