from pydantic import BaseModel
from models.document_type_model import id as id_t

class Client(BaseModel, id_t):
    id: int = None
    primer_nombre: str
    segundo_nombre: str
    primer_apellido: str
    segundo_nombre_apellido: str
    id_tipo_documento: id_t
    n_documento: str
    correo: str
    telefono: str