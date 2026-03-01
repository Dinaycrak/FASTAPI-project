from fastapi import HTTPException
from models.status_history_model import StatusHistory
from config.db_config import get_connection


def get_all_status_history():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM historial_estado")
    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


def get_status_history_by_id(id_historial: int):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM historial_estado WHERE id_historial = %s",
        (id_historial,)
    )

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    if not result:
        raise HTTPException(status_code=404, detail="Historial no encontrado")

    return result


def create_status_history(history: StatusHistory):
    connection = get_connection()
    cursor = connection.cursor()

    sql = """
        INSERT INTO historial_estado (
            id_estado_anterior,
            id_estado_nuevo,
            cambiado_por,
            fecha_cambio
        )
        VALUES (%s, %s, %s, %s)
    """

    values = (
        history.id_estado_anterior,
        history.id_estado_nuevo,
        history.cambiado_por,
        history.fecha_cambio
    )

    cursor.execute(sql, values)
    connection.commit()

    cursor.close()
    connection.close()

    return {"message": "Historial creado correctamente"}


def update_status_history(id_historial: int, history: StatusHistory):
    connection = get_connection()
    cursor = connection.cursor()

    sql = """
        UPDATE historial_estado SET
            id_estado_anterior = %s,
            id_estado_nuevo = %s,
            cambiado_por = %s,
            fecha_cambio = %s
        WHERE id_historial = %s
    """

    values = (
        history.id_estado_anterior,
        history.id_estado_nuevo,
        history.cambiado_por,
        history.fecha_cambio,
        id_historial
    )

    cursor.execute(sql, values)
    connection.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Historial no encontrado")

    cursor.close()
    connection.close()

    return {"message": "Historial actualizado correctamente"}


def delete_status_history(id_historial: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM historial_estado WHERE id_historial = %s",
        (id_historial,)
    )

    connection.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Historial no encontrado")

    cursor.close()
    connection.close()

    return {"message": "Historial eliminado correctamente"}