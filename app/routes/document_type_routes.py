from fastapi import APIRouter
from controllers.document_type_controller import DocumentTypeController
from models.document_type_model import DocumentType

router = APIRouter()

document_type_controller = DocumentTypeController()


@router.post("/document-types", response_model=dict)
async def create_document_type(document_type: DocumentType):
    return document_type_controller.create_document_type(document_type)


@router.get("/document-types/{document_type_id}", response_model=DocumentType)
async def get_document_type(document_type_id: int):
    return document_type_controller.get_document_type(document_type_id)


@router.get("/document-types", response_model=dict)
async def get_document_types():
    return document_type_controller.get_document_types()


@router.put("/document-types/{document_type_id}", response_model=dict)
async def update_document_type(document_type_id: int, document_type: DocumentType):
    return document_type_controller.update_document_type(document_type_id, document_type)


@router.delete("/document-types/{document_type_id}", response_model=dict)
async def delete_document_type(document_type_id: int):
    return document_type_controller.delete_document_type(document_type_id)