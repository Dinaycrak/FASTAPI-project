from fastapi import APIRouter
from controllers.comments_controller import *
from models.comments_model import Comments

router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)


@router.get("/")
def get_comments():
    return get_all_comments()


@router.get("/{id_comentario}")
def get_comment(id_comentario: int):
    return get_comment_by_id(id_comentario)


@router.post("/")
def create(comment: Comments):
    return create_comment(comment)


@router.put("/{id_comentario}")
def update(id_comentario: int, comment: Comments):
    return update_comment(id_comentario, comment)


@router.delete("/{id_comentario}")
def delete(id_comentario: int):
    return delete_comment(id_comentario)