from pydantic import BaseModel
from models.perfil_model import id as id_p

class User(BaseModel, id_p):
    id: int = None
    nombre: str
    apellido: str
    cedula: str
    edad: int
    usuario: str
    contrasena: str
    id_perfil: id_p