import psycopg2
import mysql
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.client_model import Client
from fastapi.encoders import jsonable_encoder

class ClientController:
        
    def create_client(self, client: Client):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO clientes (primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, id_tipo_documento, n_documento, correo, telefono) VALUES (%s, %s, %s, %s, %s ,%s)", (client.nombre, client.apellido, client.cedula, client.edad, client.usuario, client.contrasena))
            conn.commit()
            conn.close()
            return {"resultado": "Cliente creado"}
        except mysql.connector.Error as err:
            # Si falla el INSERT, los datos no quedan guardados parcialmente en la base de datos
            # Se usa para deshacer los cambios de la transacción activa cuando ocurre un error en el try.
            conn.rollback()
        finally:
            conn.close()
        

    def get_client(self, client_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clientes WHERE id = %s", (client_id,))
            result = cursor.fetchone()
            payload = []
            content = {} 
            
            content={
                    'id':int(result[0]),
                    'primer_nombre':result[1],
                    'segundo_nombre':result[2],
                    'primer_apellido':result[3],
                    'primer_apellido':result[4],
                    'id_tipo_documento':result[5],
                    'n_documento':result(result[6]),
                    'correo':result[7],
                    'telefono':result[8]
            }
            payload.append(content)
            
            json_data = jsonable_encoder(content)            
            if result:
               return  json_data
            else:
                ##Esto interrumpe la ejecución y responde al cliente con un código 404
                ## comunica al cliente de la API qué pasó (error HTTP).
                ##código 404,comportamiento correcto según las reglas HTTP
                raise HTTPException(status_code=404, detail="User not found")  
                
        except mysql.connector.Error as err:
            # Se usa para deshacer los cambios de la transacción activa cuando ocurre un error en el try.
            ##Maneja el estado de la transacción en la base de datos.Si un INSERT, UPDATE o DELETE falla dentro de una transacción, rollback() revierte esos cambios.
            conn.rollback()
        finally:
            conn.close()
       
    def get_clients(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clientes")
            result = cursor.fetchall()
            payload = []
            content = {} 
            for data in result:
                content={
                    'id':int(result[0]),
                    'primer_nombre':result[1],
                    'segundo_nombre':result[2],
                    'primer_apellido':result[3],
                    'primer_apellido':result[4],
                    'id_tipo_documento':result[5],
                    'n_documento':result(result[6]),
                    'correo':result[7],
                    'telefono':result[8]
                }
                payload.append(content)
                content = {}
            json_data = jsonable_encoder(payload)        
            if result:
               return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="User not found")  
                
        except mysql.connector.Error as err:
            conn.rollback()
        finally:
            conn.close()
    
    
       

##user_controller = UserController()