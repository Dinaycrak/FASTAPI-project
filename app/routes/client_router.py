from fastapi import APIRouter, HTTPException
from controllers.client_controller import ClientController
from models.client_model import Client

router = APIRouter()

nuevo_cliente = ClientController()


@router.post("/create_client")
async def create_client(client: Client):
    rpta = nuevo_cliente.create_client(client)
    return rpta


@router.get("/get_client/{client_id}",response_model=Client)
async def get_client(client_id: int):
    rpta = nuevo_cliente.get_client(client_id)
    return rpta

@router.get("/get_client/")
async def get_users():
    rpta = nuevo_cliente.get_clients()
    return rpta