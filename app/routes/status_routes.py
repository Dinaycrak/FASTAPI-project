from fastapi import APIRouter
from controllers.status_controller import StatusController
from models.status_model import Status

router = APIRouter()

status_controller = StatusController()


@router.post("/statuses")
async def create_status(status: Status):
    return status_controller.create_status(status)


@router.get("/statuses/{status_id}")
async def get_status(status_id: int):
    return status_controller.get_status(status_id)


@router.get("/statuses")
async def get_statuses():
    return status_controller.get_statuses()


@router.put("/statuses/{status_id}")
async def update_status(status_id: int, status: Status):
    return status_controller.update_status(status_id, status)


@router.delete("/statuses/{status_id}")
async def delete_status(status_id: int):
    return status_controller.delete_status(status_id)