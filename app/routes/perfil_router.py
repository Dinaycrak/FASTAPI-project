from fastapi import APIRouter, HTTPException
from controllers.perfil_controller import PerfilController
from models.perfil_model import Perfil

router = APIRouter()

nuevo_perfil = PerfilController()


@router.post("/create_perfil")
async def create_perfil(perfil: Perfil):
    rpta = nuevo_perfil.create_perfil(perfil)
    return rpta


@router.get("/get_perfil/{perfil_id}",response_model=Perfil)
async def get_perfil(perfil_id: int):
    rpta = nuevo_perfil.get_perfil(perfil_id)
    return rpta

@router.get("/get_perfil/")
async def get_perfil():
    rpta = nuevo_perfil.get_perfiles()
    return rpta