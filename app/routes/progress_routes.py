from fastapi import APIRouter
from controllers.progress_controller import *
from models.progress_model import Progress

router = APIRouter(prefix="/progress", tags=["Progress"])


@router.get("/")
def get_progress():
    return get_all_progress()


@router.get("/{id_avance}")
def get_progress_id(id_avance: int):
    return get_progress_by_id(id_avance)


@router.post("/")
def create(progress: Progress):
    return create_progress(progress)


@router.put("/{id_avance}")
def update(id_avance: int, progress: Progress):
    return update_progress(id_avance, progress)


@router.delete("/{id_avance}")
def delete(id_avance: int):
    return delete_progress(id_avance)