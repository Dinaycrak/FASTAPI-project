import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.status_model import Status
from fastapi.encoders import jsonable_encoder


class StatusController:

    def create_status(self, status: Status):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO estados (nombre_estado, descripcion)
                VALUES (%s, %s)
                RETURNING id_estado
            """, (
                status.nombre_estado,
                status.descripcion
            ))

            new_id = cursor.fetchone()[0]
            conn.commit()

            return {
                "resultado": "Estado creado correctamente",
                "id_estado": new_id
            }

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()


    def get_status(self, status_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id_estado, nombre_estado, descripcion
                FROM estados
                WHERE id_estado = %s
            """, (status_id,))

            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="Estado no encontrado")

            status_data = {
                "id_estado": result[0],
                "nombre_estado": result[1],
                "descripcion": result[2]
            }

            return jsonable_encoder(status_data)

        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()


    def get_statuses(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id_estado, nombre_estado, descripcion
                FROM estados
            """)

            results = cursor.fetchall()

            if not results:
                raise HTTPException(status_code=404, detail="No hay estados registrados")

            statuses = []

            for row in results:
                statuses.append({
                    "id_estado": row[0],
                    "nombre_estado": row[1],
                    "descripcion": row[2]
                })

            return {"resultado": jsonable_encoder(statuses)}

        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()


    def update_status(self, status_id: int, status: Status):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id_estado FROM estados WHERE id_estado = %s", (status_id,))
            existing_status = cursor.fetchone()

            if not existing_status:
                raise HTTPException(status_code=404, detail="Estado no encontrado")

            cursor.execute("""
                UPDATE estados
                SET nombre_estado = %s,
                    descripcion = %s
                WHERE id_estado = %s
            """, (
                status.nombre_estado,
                status.descripcion,
                status_id
            ))

            conn.commit()

            return {"resultado": "Estado actualizado correctamente"}

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()


    def delete_status(self, status_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id_estado FROM estados WHERE id_estado = %s", (status_id,))
            existing_status = cursor.fetchone()

            if not existing_status:
                raise HTTPException(status_code=404, detail="Estado no encontrado")

            cursor.execute("DELETE FROM estados WHERE id_estado = %s", (status_id,))
            conn.commit()

            return {"resultado": "Estado eliminado correctamente"}

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()