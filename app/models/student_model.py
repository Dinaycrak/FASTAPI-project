from pydantic import BaseModel
from typing import Optional


class Student(BaseModel):
    id_usuario: Optional[int] = None
    semestre: int
