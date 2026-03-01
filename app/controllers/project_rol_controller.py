import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.project_rol_model import ProjectRol
from fastapi.encoders import jsonable_encoder


class ProjectRolController:

    def create_project_rol(self, project_rol: ProjectRol):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO rol_proyecto (nombre_rol, descripcion)
                VALUES (%s, %s)
                RETURNING id_rol_proyecto
            """, (
                project_rol.nombre_rol,
                project_rol.descripcion
            ))

            new_id = cursor.fetchone()[0]
            conn.commit()

            return jsonable_encoder({
                "id_rol_proyecto": new_id,
                "nombre_rol": project_rol.nombre_rol,
                "descripcion": project_rol.descripcion
            })

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn:
                conn.close()


    def get_project_rol(self, project_rol_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id_rol_proyecto, nombre_rol, descripcion
                FROM rol_proyecto
                WHERE id_rol_proyecto = %s
            """, (project_rol_id,))

            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="Rol de proyecto no encontrado")

            return jsonable_encoder({
                "id_rol_proyecto": result[0],
                "nombre_rol": result[1],
                "descripcion": result[2]
            })

        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn:
                conn.close()


    def get_project_roles(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id_rol_proyecto, nombre_rol, descripcion
                FROM rol_proyecto
            """)

            result = cursor.fetchall()

            payload = [
                {
                    "id_rol_proyecto": row[0],
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


    def update_project_rol(self, project_rol_id: int, project_rol: ProjectRol):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT 1 FROM rol_proyecto
                WHERE id_rol_proyecto = %s
            """, (project_rol_id,))

            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Rol de proyecto no encontrado")

            cursor.execute("""
                UPDATE rol_proyecto
                SET nombre_rol = %s,
                    descripcion = %s
                WHERE id_rol_proyecto = %s
            """, (
                project_rol.nombre_rol,
                project_rol.descripcion,
                project_rol_id
            ))

            conn.commit()

            return jsonable_encoder({
                "id_rol_proyecto": project_rol_id,
                "nombre_rol": project_rol.nombre_rol,
                "descripcion": project_rol.descripcion
            })

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn:
                conn.close()


    def delete_project_rol(self, project_rol_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT 1 FROM rol_proyecto
                WHERE id_rol_proyecto = %s
            """, (project_rol_id,))

            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Rol de proyecto no encontrado")

            cursor.execute("""
                DELETE FROM rol_proyecto
                WHERE id_rol_proyecto = %s
            """, (project_rol_id,))

            conn.commit()

            return {"message": "Rol de proyecto eliminado correctamente"}

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn:
                conn.close()