import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.user_model import User
from fastapi.encoders import jsonable_encoder


class UserController:
    def create_user(self, user: User):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            #Validar que el rol exista (FK)
            if user.id_rol is not None:
                cursor.execute("SELECT id FROM roles WHERE id = %s", (user.id_rol,))
                rol = cursor.fetchone()
                if not rol:
                    raise HTTPException(status_code=400, detail="El rol no existe")

            cursor.execute("""
                INSERT INTO usuarios
                (nombre, apellido, cedula, edad, usuario, password_hash,
                 telefono, id_rol, estado_cuenta, fecha_registro)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                user.nombre,
                user.apellido,
                user.cedula,
                user.edad,
                user.usuario,
                user.password_hash,
                user.telefono,
                user.id_rol,
                user.estado_cuenta,
                user.fecha_registro
            ))

            conn.commit()

            return {"resultado": "Usuario creado correctamente"}

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()



    def get_user(self, user_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, nombre, apellido, cedula, edad, usuario,
                       password_hash, telefono, id_rol,
                       estado_cuenta, fecha_registro
                FROM usuarios
                WHERE id = %s
            """, (user_id,))

            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")

            user_data = {
                "id": result[0],
                "nombre": result[1],
                "apellido": result[2],
                "cedula": result[3],
                "edad": result[4],
                "usuario": result[5],
                "password_hash": result[6],
                "telefono": result[7],
                "id_rol": result[8],
                "estado_cuenta": result[9],
                "fecha_registro": str(result[10])
            }

            return jsonable_encoder(user_data)

        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()

    def get_users(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, nombre, apellido, cedula, edad, usuario,
                       password_hash, telefono, id_rol,
                       estado_cuenta, fecha_registro
                FROM usuarios
            """)

            results = cursor.fetchall()

            if not results:
                raise HTTPException(status_code=404, detail="No hay usuarios registrados")

            users = []

            for row in results:
                users.append({
                    "id": row[0],
                    "nombre": row[1],
                    "apellido": row[2],
                    "cedula": row[3],
                    "edad": row[4],
                    "usuario": row[5],
                    "password_hash": row[6],
                    "telefono": row[7],
                    "id_rol": row[8],
                    "estado_cuenta": row[9],
                    "fecha_registro": str(row[10])
                })

            return {"resultado": jsonable_encoder(users)}

        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()



    def update_user(self, user_id: int, user: User):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            #Verificar que el usuario exista
            cursor.execute("SELECT id FROM usuarios WHERE id = %s", (user_id,))
            existing_user = cursor.fetchone()

            if not existing_user:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")

            #Validar FK rol si se envía
            if user.id_rol is not None:
                cursor.execute("SELECT id FROM roles WHERE id = %s", (user.id_rol,))
                rol = cursor.fetchone()
                if not rol:
                    raise HTTPException(status_code=400, detail="El rol no existe")

            cursor.execute("""
                UPDATE usuarios
                SET nombre=%s,
                    apellido=%s,
                    cedula=%s,
                    edad=%s,
                    usuario=%s,
                    password_hash=%s,
                    telefono=%s,
                    id_rol=%s,
                    estado_cuenta=%s,
                    fecha_registro=%s
                WHERE id=%s
            """, (
                user.nombre,
                user.apellido,
                user.cedula,
                user.edad,
                user.usuario,
                user.password_hash,
                user.telefono,
                user.id_rol,
                user.estado_cuenta,
                user.fecha_registro,
                user_id
            ))

            conn.commit()

            return {"resultado": "Usuario actualizado correctamente"}

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()


    def delete_user(self, user_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM usuarios WHERE id = %s", (user_id,))
            existing_user = cursor.fetchone()

            if not existing_user:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")

            cursor.execute("DELETE FROM usuarios WHERE id = %s", (user_id,))
            conn.commit()

            return {"resultado": "Usuario eliminado correctamente"}

        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()