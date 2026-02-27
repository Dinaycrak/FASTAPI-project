from fastapi import APIRouter
from controllers.user_controller import UserController
from models.user_model import User

router = APIRouter(prefix="/users", tags=["Users"])

user_controller = UserController()

@router.post("/", response_model=dict)
async def create_user(user: User):
    return user_controller.create_user(user)


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    return user_controller.get_user(user_id)


@router.get("/", response_model=dict)
async def get_users():
    return user_controller.get_users()



@router.put("/{user_id}", response_model=dict)
async def update_user(user_id: int, user: User):
    return user_controller.update_user(user_id, user)


@router.delete("/{user_id}", response_model=dict)
async def delete_user(user_id: int):
    return user_controller.delete_user(user_id)