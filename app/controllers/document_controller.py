import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.document_model import Document
from fastapi.encoders import jsonable_encoder


class DocumentController:

    def create_document(self, document: Document):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id_proyecto FROM proyectos WHERE id_proyecto = %s",
                (document.id_proyecto,)
            )
            if not cursor.fetchone():
                raise HTTPException(status_code=400, detail="El proyecto no existe")

            cursor.execute(
                "SELECT id FROM usuarios WHERE id = %s",
                (document.id_usuario,)
            )
            if not cursor.fetchone():
                raise HTTPException(status_code=400, detail="El usuario no existe")

            cursor.execute(
                "SELECT id FROM tipos_documento WHERE id = %s",
                (document.id_tipo_documento,)
            )
            if not cursor.fetchone():
                raise HTTPException(status_code=400, detail="El tipo de documento no existe")

            cursor.execute("""
                INSERT INTO documentos
                (id_proyecto, id_usuario, id_tipo_documento,
                 nombre_archivo, ruta_archivo, descripcion, fecha_subida)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id_documento
            """, (
                document.id_proyecto,
                document.id_usuario,
                document.id_tipo_documento,
                document.nombre_archivo,
                document.ruta_archivo,
                document.descripcion,
                document.fecha_subida
            ))

            new_id = cursor.fetchone()[0]
            conn.commit()

            return {
                "resultado": "Documento creado correctamente",
                "id_documento": new_id
            }

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()


    def get_document(self, document_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id_documento, id_proyecto, id_usuario,
                       id_tipo_documento, nombre_archivo,
                       ruta_archivo, descripcion, fecha_subida
                FROM documentos
                WHERE id_documento = %s
            """, (document_id,))

            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="Documento no encontrado")

            document_data = {
                "id_documento": result[0],
                "id_proyecto": result[1],
                "id_usuario": result[2],
                "id_tipo_documento": result[3],
                "nombre_archivo": result[4],
                "ruta_archivo": result[5],
                "descripcion": result[6],
                "fecha_subida": result[7]
            }

            return jsonable_encoder(document_data)

        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()


    def get_documents(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id_documento, id_proyecto, id_usuario,
                       id_tipo_documento, nombre_archivo,
                       ruta_archivo, descripcion, fecha_subida
                FROM documentos
            """)

            results = cursor.fetchall()

            if not results:
                raise HTTPException(status_code=404, detail="No hay documentos registrados")

            documents = []

            for row in results:
                documents.append({
                    "id_documento": row[0],
                    "id_proyecto": row[1],
                    "id_usuario": row[2],
                    "id_tipo_documento": row[3],
                    "nombre_archivo": row[4],
                    "ruta_archivo": row[5],
                    "descripcion": row[6],
                    "fecha_subida": row[7]
                })

            return {"resultado": jsonable_encoder(documents)}

        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()


    def update_document(self, document_id: int, document: Document):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id_documento FROM documentos WHERE id_documento = %s",
                (document_id,)
            )
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Documento no encontrado")

            cursor.execute("""
                UPDATE documentos
                SET id_proyecto=%s,
                    id_usuario=%s,
                    id_tipo_documento=%s,
                    nombre_archivo=%s,
                    ruta_archivo=%s,
                    descripcion=%s,
                    fecha_subida=%s
                WHERE id_documento=%s
            """, (
                document.id_proyecto,
                document.id_usuario,
                document.id_tipo_documento,
                document.nombre_archivo,
                document.ruta_archivo,
                document.descripcion,
                document.fecha_subida,
                document_id
            ))

            conn.commit()

            return {"resultado": "Documento actualizado correctamente"}

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()


    def delete_document(self, document_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id_documento FROM documentos WHERE id_documento = %s",
                (document_id,)
            )
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Documento no encontrado")

            cursor.execute(
                "DELETE FROM documentos WHERE id_documento = %s",
                (document_id,)
            )

            conn.commit()

            return {"resultado": "Documento eliminado correctamente"}

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()