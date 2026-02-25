from fastapi import APIRouter, HTTPException
from controllers.user_controller import UserController
from models.user_model import User

router = APIRouter()

nuevo_usuario = UserController()


@router.post("/create_user")
async def create_user(user: User):
    rpta = nuevo_usuario.create_user(user)
    return rpta


@router.get("/get_user/{user_id}",response_model=User)
async def get_user(user_id: int):
    rpta = nuevo_usuario.get_user(user_id)
    return rpta

@router.get("/get_users/")
async def get_users():
    rpta = nuevo_usuario.get_users()
    return rpta

@router.put("/update_user/{user_id}",response_model=User)
async def update_user(user_id: int):
    rpta = nuevo_usuario.update_user(user_id)
    return rpta

@router.delete("/delete_user/{user_id}")
async def delete_user(user_id: int):
    rpta = nuevo_usuario.delete_user(user_id)
    return rpta

