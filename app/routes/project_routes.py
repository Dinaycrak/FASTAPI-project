from fastapi import APIRouter
from controllers.project_controller import ProjectController
from models.project_model import Project

router = APIRouter()

project_controller = ProjectController()


@router.post("/projects")
async def create_project(project: Project):
    return project_controller.create_project(project)


@router.get("/projects/{project_id}")
async def get_project(project_id: int):
    return project_controller.get_project(project_id)


@router.get("/projects")
async def get_projects():
    return project_controller.get_projects()


@router.put("/projects/{project_id}")
async def update_project(project_id: int, project: Project):
    return project_controller.update_project(project_id, project)


@router.delete("/projects/{project_id}")
async def delete_project(project_id: int):
    return project_controller.delete_project(project_id)