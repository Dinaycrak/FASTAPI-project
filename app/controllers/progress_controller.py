from fastapi import HTTPException
from models.progress_model import Progress
from config.db_config import get_connection


def get_all_progress():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM avance")
    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


def get_progress_by_id(id_avance: int):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM avance WHERE id_avance = %s", (id_avance,))
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    if not result:
        raise HTTPException(status_code=404, detail="Avance no encontrado")

    return result


def create_progress(progress: Progress):
    connection = get_connection()
    cursor = connection.cursor()

    sql = """
        INSERT INTO avance (
            id_proyecto,
            id_usuario,
            descripcion,
            porcentaje_avance,
            fecha_registro
        )
        VALUES (%s, %s, %s, %s, %s)
    """

    values = (
        progress.id_proyecto,
        progress.id_usuario,
        progress.descripcion,
        progress.porcentaje_avance,
        progress.fecha_registro
    )

    cursor.execute(sql, values)
    connection.commit()

    cursor.close()
    connection.close()

    return {"message": "Avance creado correctamente"}


def update_progress(id_avance: int, progress: Progress):
    connection = get_connection()
    cursor = connection.cursor()

    sql = """
        UPDATE avance SET
            id_proyecto = %s,
            id_usuario = %s,
            descripcion = %s,
            porcentaje_avance = %s,
            fecha_registro = %s
        WHERE id_avance = %s
    """

    values = (
        progress.id_proyecto,
        progress.id_usuario,
        progress.descripcion,
        progress.porcentaje_avance,
        progress.fecha_registro,
        id_avance
    )

    cursor.execute(sql, values)
    connection.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Avance no encontrado")

    cursor.close()
    connection.close()

    return {"message": "Avance actualizado correctamente"}


def delete_progress(id_avance: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM avance WHERE id_avance = %s", (id_avance,))
    connection.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Avance no encontrado")

    cursor.close()
    connection.close()

    return {"message": "Avance eliminado correctamente"}