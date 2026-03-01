from fastapi import APIRouter
from controllers.status_history_controller import *
from models.status_history_model import StatusHistory

router = APIRouter(
    prefix="/status-history",
    tags=["Status History"]
)


@router.get("/")
def get_status_history():
    return get_all_status_history()


@router.get("/{id_historial}")
def get_status_history_id(id_historial: int):
    return get_status_history_by_id(id_historial)


@router.post("/")
def create(history: StatusHistory):
    return create_status_history(history)


@router.put("/{id_historial}")
def update(id_historial: int, history: StatusHistory):
    return update_status_history(id_historial, history)


@router.delete("/{id_historial}")
def delete(id_historial: int):
    return delete_status_history(id_historial)