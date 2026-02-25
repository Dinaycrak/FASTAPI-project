from fastapi import APIRouter, HTTPException
from controllers.document_type_controller import DocumentTypeController
from models.document_type_model import DocumentType

router = APIRouter()

nuevo_tipo_documento = DocumentTypeController()


@router.post("/create_document_type")
async def create_document_type(document_type: DocumentType):
    rpta = nuevo_tipo_documento.create_document_type(document_type)
    return rpta


@router.get("/get_document_type/{document_type_id}",response_model=DocumentType)
async def get_document_type(document_type_id: int):
    rpta = nuevo_tipo_documento.get_document_type(document_type_id)
    return rpta

@router.get("/get_document_type/")
async def get_document_type():
    rpta = nuevo_tipo_documento.get_document_type()
    return rpta