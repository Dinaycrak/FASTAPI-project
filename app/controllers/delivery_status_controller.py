import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.delivery_status_model import DeliveryStatus
from fastapi.encoders import jsonable_encoder


class DeliveryStatusController:

    def create_delivery_status(self, delivery_status: DeliveryStatus):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO estado_entrega (nombre_estado, descripcion)
                VALUES (%s, %s)
                RETURNING id_estado_entrega
            """, (
                delivery_status.nombre_estado,
                delivery_status.descripcion
            ))

            new_id = cursor.fetchone()[0]
            conn.commit()

            return jsonable_encoder({
                "id_estado_entrega": new_id,
                "nombre_estado": delivery_status.nombre_estado,
                "descripcion": delivery_status.descripcion
            })

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn:
                conn.close()


    def get_delivery_status(self, delivery_status_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id_estado_entrega, nombre_estado, descripcion
                FROM estado_entrega
                WHERE id_estado_entrega = %s
            """, (delivery_status_id,))

            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="Estado de entrega no encontrado")

            return jsonable_encoder({
                "id_estado_entrega": result[0],
                "nombre_estado": result[1],
                "descripcion": result[2]
            })

        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn:
                conn.close()


    def get_delivery_statuses(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id_estado_entrega, nombre_estado, descripcion
                FROM estado_entrega
            """)

            result = cursor.fetchall()

            payload = [
                {
                    "id_estado_entrega": row[0],
                    "nombre_estado": row[1],
                    "descripcion": row[2]
                }
                for row in result
            ]

            return jsonable_encoder(payload)

        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn:
                conn.close()


    def update_delivery_status(self, delivery_status_id: int, delivery_status: DeliveryStatus):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT 1 FROM estado_entrega
                WHERE id_estado_entrega = %s
            """, (delivery_status_id,))

            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Estado de entrega no encontrado")

            cursor.execute("""
                UPDATE estado_entrega
                SET nombre_estado = %s,
                    descripcion = %s
                WHERE id_estado_entrega = %s
            """, (
                delivery_status.nombre_estado,
                delivery_status.descripcion,
                delivery_status_id
            ))

            conn.commit()

            return jsonable_encoder({
                "id_estado_entrega": delivery_status_id,
                "nombre_estado": delivery_status.nombre_estado,
                "descripcion": delivery_status.descripcion
            })

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn:
                conn.close()


    def delete_delivery_status(self, delivery_status_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT 1 FROM estado_entrega
                WHERE id_estado_entrega = %s
            """, (delivery_status_id,))

            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Estado de entrega no encontrado")

            cursor.execute("""
                DELETE FROM estado_entrega
                WHERE id_estado_entrega = %s
            """, (delivery_status_id,))

            conn.commit()

            return {"message": "Estado de entrega eliminado correctamente"}

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn:
                conn.close()