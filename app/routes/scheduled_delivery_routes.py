from fastapi import APIRouter
from controllers.scheduled_delivery_controller import *
from models.scheduled_delivery_model import ScheduledDelivery

router = APIRouter(
    prefix="/scheduled-delivery",
    tags=["Scheduled Delivery"]
)


@router.get("/")
def get_scheduled_deliveries():
    return get_all_scheduled_deliveries()


@router.get("/{id_entrega}")
def get_scheduled_delivery(id_entrega: int):
    return get_scheduled_delivery_by_id(id_entrega)


@router.post("/")
def create_scheduled_delivery_route(delivery: ScheduledDelivery):
    return create_scheduled_delivery(delivery)


@router.put("/{id_entrega}")
def update_scheduled_delivery_route(id_entrega: int, delivery: ScheduledDelivery):
    return update_scheduled_delivery(id_entrega, delivery)


@router.delete("/{id_entrega}")
def delete_scheduled_delivery_route(id_entrega: int):
    return delete_scheduled_delivery(id_entrega)