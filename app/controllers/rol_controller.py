import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.rol_model import User  # si decides renombrarlo a Rol, cambia aquí
from fastapi.encoders import jsonable_encoder


class RolController:

    def create_rol(self, rol: User):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO rol (nombre_rol, descripcion)
                VALUES (%s, %s)
                RETURNING id_rol
            """, (
                rol.nombre_rol,
                rol.descripcion
            ))

            new_id = cursor.fetchone()[0]
            conn.commit()

            return jsonable_encoder({
                "id_rol": new_id,
                "nombre_rol": rol.nombre_rol,
                "descripcion": rol.descripcion
            })

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()


    def get_rol(self, rol_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id_rol, nombre_rol, descripcion
                FROM rol
                WHERE id_rol = %s
            """, (rol_id,))

            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="Rol no encontrado")

            return jsonable_encoder({
                "id_rol": result[0],
                "nombre_rol": result[1],
                "descripcion": result[2]
            })

        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()


    def get_roles(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id_rol, nombre_rol, descripcion
                FROM rol
            """)

            result = cursor.fetchall()

            payload = [
                {
                    "id_rol": row[0],
                    "nombre_rol": row[1],
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


    def update_rol(self, rol_id: int, rol: User):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT 1 FROM rol
                WHERE id_rol = %s
            """, (rol_id,))

            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Rol no encontrado")

            cursor.execute("""
                UPDATE rol
                SET nombre_rol = %s,
                    descripcion = %s
                WHERE id_rol = %s
            """, (
                rol.nombre_rol,
                rol.descripcion,
                rol_id
            ))

            conn.commit()

            return jsonable_encoder({
                "id_rol": rol_id,
                "nombre_rol": rol.nombre_rol,
                "descripcion": rol.descripcion
            })

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()


    def delete_rol(self, rol_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT 1 FROM rol
                WHERE id_rol = %s
            """, (rol_id,))

            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Rol no encontrado")

            cursor.execute("""
                DELETE FROM rol
                WHERE id_rol = %s
            """, (rol_id,))

            conn.commit()

            return {"message": "Rol eliminado correctamente"}

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()