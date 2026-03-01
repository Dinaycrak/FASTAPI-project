import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.user_project_model import UserProject
from fastapi.encoders import jsonable_encoder


class UserProjectController:

    def create_user_project(self, user_project: UserProject):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id_proyecto FROM proyectos WHERE id_proyecto = %s",
                (user_project.id_proyecto,)
            )
            if not cursor.fetchone():
                raise HTTPException(status_code=400, detail="El proyecto no existe")

            cursor.execute(
                "SELECT id FROM usuarios WHERE id = %s",
                (user_project.id_usuario,)
            )
            if not cursor.fetchone():
                raise HTTPException(status_code=400, detail="El usuario no existe")

            cursor.execute(
                "SELECT id_rol_proyecto FROM roles_proyecto WHERE id_rol_proyecto = %s",
                (user_project.id_rol_proyecto,)
            )
            if not cursor.fetchone():
                raise HTTPException(status_code=400, detail="El rol del proyecto no existe")

            cursor.execute("""
                INSERT INTO proyecto_usuario
                (id_proyecto, id_usuario, id_rol_proyecto, fecha_asignacion)
                VALUES (%s, %s, %s, %s)
                RETURNING id_proyecto_usuario
            """, (
                user_project.id_proyecto,
                user_project.id_usuario,
                user_project.id_rol_proyecto,
                user_project.fecha_asignacion
            ))

            new_id = cursor.fetchone()[0]
            conn.commit()

            return {
                "resultado": "Usuario asignado al proyecto correctamente",
                "id_proyecto_usuario": new_id
            }

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()


    def get_user_project(self, user_project_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id_proyecto_usuario,
                       id_proyecto,
                       id_usuario,
                       id_rol_proyecto,
                       fecha_asignacion
                FROM proyecto_usuario
                WHERE id_proyecto_usuario = %s
            """, (user_project_id,))

            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="Asignación no encontrada")

            data = {
                "id_proyecto_usuario": result[0],
                "id_proyecto": result[1],
                "id_usuario": result[2],
                "id_rol_proyecto": result[3],
                "fecha_asignacion": result[4]
            }

            return jsonable_encoder(data)

        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()


    def get_user_projects(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id_proyecto_usuario,
                       id_proyecto,
                       id_usuario,
                       id_rol_proyecto,
                       fecha_asignacion
                FROM proyecto_usuario
            """)

            results = cursor.fetchall()

            if not results:
                raise HTTPException(status_code=404, detail="No hay asignaciones registradas")

            assignments = []

            for row in results:
                assignments.append({
                    "id_proyecto_usuario": row[0],
                    "id_proyecto": row[1],
                    "id_usuario": row[2],
                    "id_rol_proyecto": row[3],
                    "fecha_asignacion": row[4]
                })

            return {"resultado": jsonable_encoder(assignments)}

        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()


    def update_user_project(self, user_project_id: int, user_project: UserProject):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id_proyecto_usuario FROM proyecto_usuario WHERE id_proyecto_usuario = %s",
                (user_project_id,)
            )
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Asignación no encontrada")

            cursor.execute("""
                UPDATE proyecto_usuario
                SET id_proyecto = %s,
                    id_usuario = %s,
                    id_rol_proyecto = %s,
                    fecha_asignacion = %s
                WHERE id_proyecto_usuario = %s
            """, (
                user_project.id_proyecto,
                user_project.id_usuario,
                user_project.id_rol_proyecto,
                user_project.fecha_asignacion,
                user_project_id
            ))

            conn.commit()

            return {"resultado": "Asignación actualizada correctamente"}

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()


    def delete_user_project(self, user_project_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id_proyecto_usuario FROM proyecto_usuario WHERE id_proyecto_usuario = %s",
                (user_project_id,)
            )
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Asignación no encontrada")

            cursor.execute(
                "DELETE FROM proyecto_usuario WHERE id_proyecto_usuario = %s",
                (user_project_id,)
            )

            conn.commit()

            return {"resultado": "Asignación eliminada correctamente"}

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()