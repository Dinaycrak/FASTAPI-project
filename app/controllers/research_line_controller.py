import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.research_line_model import ResearchLine
from fastapi.encoders import jsonable_encoder


class ResearchLineController:

    def create_research_line(self, research_line: ResearchLine):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO linea_investigacion (nombre_linea, descripcion)
                VALUES (%s, %s)
                RETURNING id_linea
            """, (
                research_line.nombre_linea,
                research_line.descripcion
            ))

            new_id = cursor.fetchone()[0]
            conn.commit()

            return jsonable_encoder({
                "id_linea": new_id,
                "nombre_linea": research_line.nombre_linea,
                "descripcion": research_line.descripcion
            })

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn:
                conn.close()


    def get_research_line(self, research_line_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id_linea, nombre_linea, descripcion
                FROM linea_investigacion
                WHERE id_linea = %s
            """, (research_line_id,))

            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="Línea no encontrada")

            return jsonable_encoder({
                "id_linea": result[0],
                "nombre_linea": result[1],
                "descripcion": result[2]
            })

        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn:
                conn.close()


    def get_research_lines(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id_linea, nombre_linea, descripcion
                FROM linea_investigacion
            """)

            result = cursor.fetchall()

            payload = [
                {
                    "id_linea": row[0],
                    "nombre_linea": row[1],
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


    def update_research_line(self, research_line_id: int, research_line: ResearchLine):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT 1 FROM linea_investigacion
                WHERE id_linea = %s
            """, (research_line_id,))

            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Línea no encontrada")

            cursor.execute("""
                UPDATE linea_investigacion
                SET nombre_linea = %s,
                    descripcion = %s
                WHERE id_linea = %s
            """, (
                research_line.nombre_linea,
                research_line.descripcion,
                research_line_id
            ))

            conn.commit()

            return jsonable_encoder({
                "id_linea": research_line_id,
                "nombre_linea": research_line.nombre_linea,
                "descripcion": research_line.descripcion
            })

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn:
                conn.close()


    def delete_research_line(self, research_line_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT 1 FROM linea_investigacion
                WHERE id_linea = %s
            """, (research_line_id,))

            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Línea no encontrada")

            cursor.execute("""
                DELETE FROM linea_investigacion
                WHERE id_linea = %s
            """, (research_line_id,))

            conn.commit()

            return {"message": "Línea eliminada correctamente"}

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn:
                conn.close()