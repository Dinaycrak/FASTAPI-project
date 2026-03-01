from fastapi import APIRouter
from typing import List
from controllers.project_rol_controller import ProjectRolController
from models.project_rol_model import ProyectRol

router = APIRouter()

project_rol_controller = ProjectRolController()


@router.post("/project-roles", response_model=ProyectRol)
async def create_project_rol(project_rol: ProyectRol):
    return project_rol_controller.create_project_rol(project_rol)


@router.get("/project-roles/{project_rol_id}", response_model=ProyectRol)
async def get_project_rol(project_rol_id: int):
    return project_rol_controller.get_project_rol(project_rol_id)


@router.get("/project-roles", response_model=List[ProyectRol])
async def get_project_roles():
    return project_rol_controller.get_project_roles()


@router.put("/project-roles/{project_rol_id}", response_model=ProyectRol)
async def update_project_rol(project_rol_id: int, project_rol: ProyectRol):
    return project_rol_controller.update_project_rol(project_rol_id, project_rol)


@router.delete("/project-roles/{project_rol_id}")
async def delete_project_rol(project_rol_id: int):
    return project_rol_controller.delete_project_rol(project_rol_id)