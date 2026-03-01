from fastapi import APIRouter
from typing import List
from controllers.research_line_controller import ResearchLineController
from models.research_line_model import ResearchLine

router = APIRouter()

research_line_controller = ResearchLineController()


@router.post("/research-lines", response_model=ResearchLine)
async def create_research_line(research_line: ResearchLine):
    return research_line_controller.create_research_line(research_line)


@router.get("/research-lines/{research_line_id}", response_model=ResearchLine)
async def get_research_line(research_line_id: int):
    return research_line_controller.get_research_line(research_line_id)


@router.get("/research-lines", response_model=List[ResearchLine])
async def get_research_lines():
    return research_line_controller.get_research_lines()


@router.put("/research-lines/{research_line_id}", response_model=ResearchLine)
async def update_research_line(research_line_id: int, research_line: ResearchLine):
    return research_line_controller.update_research_line(research_line_id, research_line)


@router.delete("/research-lines/{research_line_id}")
async def delete_research_line(research_line_id: int):
    return research_line_controller.delete_research_line(research_line_id)