from fastapi import HTTPException
from models.comments_model import Comments
from config.db_config import get_connection


def get_all_comments():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM comentarios")
    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


def get_comment_by_id(id_comentario: int):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM comentarios WHERE id_comentario = %s",
        (id_comentario,)
    )

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    if not result:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")

    return result


def create_comment(comment: Comments):
    connection = get_connection()
    cursor = connection.cursor()

    sql = """
        INSERT INTO comentarios (
            id_avance,
            id_usuario,
            contenido,
            fecha_comentario
        )
        VALUES (%s, %s, %s, %s)
    """

    values = (
        comment.id_avance,
        comment.id_usuario,
        comment.contenido,
        comment.fecha_comentario
    )

    cursor.execute(sql, values)
    connection.commit()

    cursor.close()
    connection.close()

    return {"message": "Comentario creado correctamente"}


def update_comment(id_comentario: int, comment: Comments):
    connection = get_connection()
    cursor = connection.cursor()

    sql = """
        UPDATE comentarios SET
            id_avance = %s,
            id_usuario = %s,
            contenido = %s,
            fecha_comentario = %s
        WHERE id_comentario = %s
    """

    values = (
        comment.id_avance,
        comment.id_usuario,
        comment.contenido,
        comment.fecha_comentario,
        id_comentario
    )

    cursor.execute(sql, values)
    connection.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")

    cursor.close()
    connection.close()

    return {"message": "Comentario actualizado correctamente"}


def delete_comment(id_comentario: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM comentarios WHERE id_comentario = %s",
        (id_comentario,)
    )

    connection.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")

    cursor.close()
    connection.close()

    return {"message": "Comentario eliminado correctamente"}