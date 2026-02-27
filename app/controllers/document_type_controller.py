import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.document_type_model import DocumentType
from fastapi.encoders import jsonable_encoder


class DocumentTypeController:

    def create_document_type(self, document_type: DocumentType):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO tipo_documento (nombre_tipo, descripcion)
                VALUES (%s, %s)
                RETURNING id_tipo_documento
            """, (
                document_type.nombre_tipo,
                document_type.descripcion
            ))

            new_id = cursor.fetchone()[0]
            conn.commit()

            return jsonable_encoder({
                "id_tipo_documento": new_id,
                "nombre_tipo": document_type.nombre_tipo,
                "descripcion": document_type.descripcion
            })

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()


    def get_document_type(self, document_type_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id_tipo_documento, nombre_tipo, descripcion
                FROM tipo_documento
                WHERE id_tipo_documento = %s
            """, (document_type_id,))

            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="Document type not found")

            return jsonable_encoder({
                "id_tipo_documento": result[0],
                "nombre_tipo": result[1],
                "descripcion": result[2]
            })

        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()


    def get_document_types(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id_tipo_documento, nombre_tipo, descripcion
                FROM tipo_documento
            """)

            result = cursor.fetchall()

            payload = [
                {
                    "id_tipo_documento": row[0],
                    "nombre_tipo": row[1],
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


    def update_document_type(self, document_type_id: int, document_type: DocumentType):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT 1 FROM tipo_documento
                WHERE id_tipo_documento = %s
            """, (document_type_id,))

            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Document type not found")

            cursor.execute("""
                UPDATE tipo_documento
                SET nombre_tipo = %s,
                    descripcion = %s
                WHERE id_tipo_documento = %s
            """, (
                document_type.nombre_tipo,
                document_type.descripcion,
                document_type_id
            ))

            conn.commit()

            return jsonable_encoder({
                "id_tipo_documento": document_type_id,
                "nombre_tipo": document_type.nombre_tipo,
                "descripcion": document_type.descripcion
            })

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()


    def delete_document_type(self, document_type_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT 1 FROM tipo_documento
                WHERE id_tipo_documento = %s
            """, (document_type_id,))

            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Document type not found")

            cursor.execute("""
                DELETE FROM tipo_documento
                WHERE id_tipo_documento = %s
            """, (document_type_id,))

            conn.commit()

            return {"message": "Tipo de documento eliminado correctamente"}

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()