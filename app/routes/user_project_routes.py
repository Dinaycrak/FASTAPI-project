from fastapi import APIRouter
from controllers.user_project_controller import UserProjectController
from models.user_project_model import UserProject

router = APIRouter()

user_project_controller = UserProjectController()


@router.post("/user-projects")
async def create_user_project(user_project: UserProject):
    return user_project_controller.create_user_project(user_project)


@router.get("/user-projects/{user_project_id}")
async def get_user_project(user_project_id: int):
    return user_project_controller.get_user_project(user_project_id)


@router.get("/user-projects")
async def get_user_projects():
    return user_project_controller.get_user_projects()


@router.put("/user-projects/{user_project_id}")
async def update_user_project(user_project_id: int, user_project: UserProject):
    return user_project_controller.update_user_project(user_project_id, user_project)


@router.delete("/user-projects/{user_project_id}")
async def delete_user_project(user_project_id: int):
    return user_project_controller.delete_user_project(user_project_id)