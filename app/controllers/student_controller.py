import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.student_model import Student
from fastapi.encoders import jsonable_encoder


class StudentController:

    def create_student(self, student: Student):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM usuarios WHERE id = %s", (student.id_usuario,))
            user = cursor.fetchone()

            if not user:
                raise HTTPException(status_code=400, detail="El usuario no existe")

            cursor.execute("""
                INSERT INTO estudiantes (id_usuario, semestre)
                VALUES (%s, %s)
            """, (
                student.id_usuario,
                student.semestre
            ))

            conn.commit()

            return {"resultado": "Estudiante creado correctamente"}

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()


    def get_student(self, student_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id_usuario, semestre
                FROM estudiantes
                WHERE id_usuario = %s
            """, (student_id,))

            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="Estudiante no encontrado")

            student_data = {
                "id_usuario": result[0],
                "semestre": result[1]
            }

            return jsonable_encoder(student_data)

        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()


    def get_students(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id_usuario, semestre
                FROM estudiantes
            """)

            results = cursor.fetchall()

            if not results:
                raise HTTPException(status_code=404, detail="No hay estudiantes registrados")

            students = []

            for row in results:
                students.append({
                    "id_usuario": row[0],
                    "semestre": row[1]
                })

            return {"resultado": jsonable_encoder(students)}

        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()


    def update_student(self, student_id: int, student: Student):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id_usuario FROM estudiantes WHERE id_usuario = %s", (student_id,))
            existing_student = cursor.fetchone()

            if not existing_student:
                raise HTTPException(status_code=404, detail="Estudiante no encontrado")

            cursor.execute("""
                UPDATE estudiantes
                SET semestre = %s
                WHERE id_usuario = %s
            """, (
                student.semestre,
                student_id
            ))

            conn.commit()

            return {"resultado": "Estudiante actualizado correctamente"}

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()


    def delete_student(self, student_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id_usuario FROM estudiantes WHERE id_usuario = %s", (student_id,))
            existing_student = cursor.fetchone()

            if not existing_student:
                raise HTTPException(status_code=404, detail="Estudiante no encontrado")

            cursor.execute("DELETE FROM estudiantes WHERE id_usuario = %s", (student_id,))
            conn.commit()

            return {"resultado": "Estudiante eliminado correctamente"}

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()