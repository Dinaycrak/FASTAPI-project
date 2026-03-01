import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.project_model import Project
from fastapi.encoders import jsonable_encoder


class ProjectController:

    def create_project(self, project: Project):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            if project.id_estado is not None:
                cursor.execute(
                    "SELECT id_estado FROM estados WHERE id_estado = %s",
                    (project.id_estado,)
                )
                estado = cursor.fetchone()
                if not estado:
                    raise HTTPException(status_code=400, detail="El estado no existe")

            if project.id_linea is not None:
                cursor.execute(
                    "SELECT id_linea FROM lineas_investigacion WHERE id_linea = %s",
                    (project.id_linea,)
                )
                linea = cursor.fetchone()
                if not linea:
                    raise HTTPException(status_code=400, detail="La línea de investigación no existe")

            cursor.execute("""
                INSERT INTO proyectos
                (nombre_proyecto, descripcion, fecha_inicio, fecha_fin,
                 id_estado, id_linea, creado_por, fecha_creacion)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id_proyecto
            """, (
                project.nombre_proyecto,
                project.descripcion,
                project.fecha_inicio,
                project.fecha_fin,
                project.id_estado,
                project.id_linea,
                project.creado_por,
                project.fecha_creacion
            ))

            new_id = cursor.fetchone()[0]
            conn.commit()

            return {
                "resultado": "Proyecto creado correctamente",
                "id_proyecto": new_id
            }

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()


    def get_project(self, project_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id_proyecto, nombre_proyecto, descripcion,
                       fecha_inicio, fecha_fin,
                       id_estado, id_linea,
                       creado_por, fecha_creacion
                FROM proyectos
                WHERE id_proyecto = %s
            """, (project_id,))

            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="Proyecto no encontrado")

            project_data = {
                "id_proyecto": result[0],
                "nombre_proyecto": result[1],
                "descripcion": result[2],
                "fecha_inicio": result[3],
                "fecha_fin": result[4],
                "id_estado": result[5],
                "id_linea": result[6],
                "creado_por": result[7],
                "fecha_creacion": result[8]
            }

            return jsonable_encoder(project_data)

        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()


    def get_projects(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id_proyecto, nombre_proyecto, descripcion,
                       fecha_inicio, fecha_fin,
                       id_estado, id_linea,
                       creado_por, fecha_creacion
                FROM proyectos
            """)

            results = cursor.fetchall()

            if not results:
                raise HTTPException(status_code=404, detail="No hay proyectos registrados")

            projects = []

            for row in results:
                projects.append({
                    "id_proyecto": row[0],
                    "nombre_proyecto": row[1],
                    "descripcion": row[2],
                    "fecha_inicio": row[3],
                    "fecha_fin": row[4],
                    "id_estado": row[5],
                    "id_linea": row[6],
                    "creado_por": row[7],
                    "fecha_creacion": row[8]
                })

            return {"resultado": jsonable_encoder(projects)}

        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()


    def update_project(self, project_id: int, project: Project):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id_proyecto FROM proyectos WHERE id_proyecto = %s",
                (project_id,)
            )
            existing = cursor.fetchone()

            if not existing:
                raise HTTPException(status_code=404, detail="Proyecto no encontrado")

            cursor.execute("""
                UPDATE proyectos
                SET nombre_proyecto=%s,
                    descripcion=%s,
                    fecha_inicio=%s,
                    fecha_fin=%s,
                    id_estado=%s,
                    id_linea=%s,
                    creado_por=%s,
                    fecha_creacion=%s
                WHERE id_proyecto=%s
            """, (
                project.nombre_proyecto,
                project.descripcion,
                project.fecha_inicio,
                project.fecha_fin,
                project.id_estado,
                project.id_linea,
                project.creado_por,
                project.fecha_creacion,
                project_id
            ))

            conn.commit()

            return {"resultado": "Proyecto actualizado correctamente"}

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()


    def delete_project(self, project_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id_proyecto FROM proyectos WHERE id_proyecto = %s",
                (project_id,)
            )
            existing = cursor.fetchone()

            if not existing:
                raise HTTPException(status_code=404, detail="Proyecto no encontrado")

            cursor.execute(
                "DELETE FROM proyectos WHERE id_proyecto = %s",
                (project_id,)
            )

            conn.commit()

            return {"resultado": "Proyecto eliminado correctamente"}

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()