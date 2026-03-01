from fastapi import APIRouter
from typing import List
from controllers.rol_controller import RolController
from models.rol_model import Rol

router = APIRouter()

rol_controller = RolController()


@router.post("/roles", response_model=Rol)
async def create_rol(rol: Rol):
    return rol_controller.create_rol(rol)


@router.get("/roles/{rol_id}", response_model=Rol)
async def get_rol(rol_id: int):
    return rol_controller.get_rol(rol_id)


@router.get("/roles", response_model=List[Rol])
async def get_roles():
    return rol_controller.get_roles()


@router.put("/roles/{rol_id}", response_model=Rol)
async def update_rol(rol_id: int, rol: Rol):
    return rol_controller.update_rol(rol_id, rol)


@router.delete("/roles/{rol_id}")
async def delete_rol(rol_id: int):
    return rol_controller.delete_rol(rol_id)