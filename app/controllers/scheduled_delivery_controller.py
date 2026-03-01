from fastapi import HTTPException
from models.scheduled_delivery_model import ScheduledDelivery
from config.db_config import get_connection


def get_all_scheduled_deliveries():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM entrega_programada")
    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


def get_scheduled_delivery_by_id(id_entrega: int):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM entrega_programada WHERE id_entrega = %s",
        (id_entrega,)
    )

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    if not result:
        raise HTTPException(status_code=404, detail="Entrega programada no encontrada")

    return result


def create_scheduled_delivery(delivery: ScheduledDelivery):
    connection = get_connection()
    cursor = connection.cursor()

    sql = """
        INSERT INTO entrega_programada (
            id_proyecto,
            fecha_limite,
            descripcion,
            id_estado_entrega
        )
        VALUES (%s, %s, %s, %s)
    """

    values = (
        delivery.id_proyecto,
        delivery.fecha_limite,
        delivery.descripcion,
        delivery.id_estado_entrega
    )

    cursor.execute(sql, values)
    connection.commit()

    cursor.close()
    connection.close()

    return {"message": "Entrega programada creada correctamente"}


def update_scheduled_delivery(id_entrega: int, delivery: ScheduledDelivery):
    connection = get_connection()
    cursor = connection.cursor()

    sql = """
        UPDATE entrega_programada SET
            id_proyecto = %s,
            fecha_limite = %s,
            descripcion = %s,
            id_estado_entrega = %s
        WHERE id_entrega = %s
    """

    values = (
        delivery.id_proyecto,
        delivery.fecha_limite,
        delivery.descripcion,
        delivery.id_estado_entrega,
        id_entrega
    )

    cursor.execute(sql, values)
    connection.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Entrega programada no encontrada")

    cursor.close()
    connection.close()

    return {"message": "Entrega programada actualizada correctamente"}


def delete_scheduled_delivery(id_entrega: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM entrega_programada WHERE id_entrega = %s",
        (id_entrega,)
    )

    connection.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Entrega programada no encontrada")

    cursor.close()
    connection.close()

    return {"message": "Entrega programada eliminada correctamente"}