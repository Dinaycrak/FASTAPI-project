from pydantic import BaseModel

class Perfil(BaseModel):
    id: int = None
    nombre: str
    descripcion: str