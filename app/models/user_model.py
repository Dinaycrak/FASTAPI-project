from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class User(BaseModel):
    id_usuario: Optional[int] = None
    nombre: str
    apellido: str
    cedula: str
    edad: int
    usuario: str
    password_hash: str
    telefono: int
    id_rol: Optional[int] = None
    estado_cuenta: bool
    fecha_registro: datetime