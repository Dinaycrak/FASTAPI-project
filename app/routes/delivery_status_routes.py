from fastapi import APIRouter
from typing import List
from controllers.delivery_status_controller import DeliveryStatusController
from models.delivery_status_model import DeliveryStatus

router = APIRouter()

delivery_status_controller = DeliveryStatusController()


@router.post("/delivery-status", response_model=DeliveryStatus)
async def create_delivery_status(delivery_status: DeliveryStatus):
    return delivery_status_controller.create_delivery_status(delivery_status)


@router.get("/delivery-status/{delivery_status_id}", response_model=DeliveryStatus)
async def get_delivery_status(delivery_status_id: int):
    return delivery_status_controller.get_delivery_status(delivery_status_id)


@router.get("/delivery-status", response_model=List[DeliveryStatus])
async def get_delivery_statuses():
    return delivery_status_controller.get_delivery_statuses()


@router.put("/delivery-status/{delivery_status_id}", response_model=DeliveryStatus)
async def update_delivery_status(delivery_status_id: int, delivery_status: DeliveryStatus):
    return delivery_status_controller.update_delivery_status(delivery_status_id, delivery_status)


@router.delete("/delivery-status/{delivery_status_id}")
async def delete_delivery_status(delivery_status_id: int):
    return delivery_status_controller.delete_delivery_status(delivery_status_id)