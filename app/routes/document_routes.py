from fastapi import APIRouter
from controllers.document_controller import DocumentController
from models.document_model import Document

router = APIRouter()

document_controller = DocumentController()


@router.post("/documents")
async def create_document(document: Document):
    return document_controller.create_document(document)


@router.get("/documents/{document_id}")
async def get_document(document_id: int):
    return document_controller.get_document(document_id)


@router.get("/documents")
async def get_documents():
    return document_controller.get_documents()


@router.put("/documents/{document_id}")
async def update_document(document_id: int, document: Document):
    return document_controller.update_document(document_id, document)


@router.delete("/documents/{document_id}")
async def delete_document(document_id: int):
    return document_controller.delete_document(document_id)