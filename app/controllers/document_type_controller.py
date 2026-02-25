import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from app.models.document_type_model import DocumentType
from fastapi.encoders import jsonable_encoder

class DocumentTypeController:
        
    def create_document_type(self, document_type: DocumentType):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tipo_documento (nombre_tipo, descripcion) VALUES (%s, %s)", (document_type.nombre_tipo, document_type.descripcion))
            conn.commit()
            conn.close()
            return {"resultado": "tipo de documento guardado"}
        except psycopg2.connector.Error as err:
            # Si falla el INSERT, los datos no quedan guardados parcialmente en la base de datos
            # Se usa para deshacer los cambios de la transacción activa cuando ocurre un error en el try.
            conn.rollback()
        finally:
            conn.close()
        

    def get_document_type(self, document_type_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tipo_documento WHERE id = %s", (document_type_id,))
            result = cursor.fetchone()
            payload = []
            content = {} 
            
            content={
                    'id':int(result[0]),
                    'nombre_tipo':result[1],
                    'descripcion':result[2]
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
                
        except psycopg2.connector.Error as err:
            # Se usa para deshacer los cambios de la transacción activa cuando ocurre un error en el try.
            ##Maneja el estado de la transacción en la base de datos.Si un INSERT, UPDATE o DELETE falla dentro de una transacción, rollback() revierte esos cambios.
            conn.rollback()
        finally:
            conn.close()
       
    def get_tipos_documentos(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tipo_documento")
            result = cursor.fetchall()
            payload = []
            content = {} 
            for data in result:
                content={
                    'id':data[0],
                    'nombre_tipo':data[1],
                    'descipcion':data[2]
                }
                payload.append(content)
                content = {}
            json_data = jsonable_encoder(payload)        
            if result:
               return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="User not found")  
                
        except psycopg2.connector.Error as err:
            conn.rollback()
        finally:
            conn.close()
    
    
       

##document_type_controller = DocumentTypeController()