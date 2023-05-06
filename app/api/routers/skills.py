from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.crud import skills as crud
from api.crud.utils import UniqueIdException, ItemNotFoundException
from api.schemas import Skill as SkillSchema
from api.utils import get_db

router = APIRouter(
    prefix="/skills",
    tags=["skills"],
    responses={409: {"description": "Key not unique"},
        404: {"description": "Not found"}},
)

@router.post("/", response_model=SkillSchema)
def insert_skill(skill: SkillSchema, db: Session = Depends(get_db)):
    try:
        db_skill = crud.create_skill(skill, db=db)
    except UniqueIdException:
        raise HTTPException(409, "skill id already exists in database.")
    return SkillSchema.parse_orm(db_skill)

@router.delete("/{skill_id}")
def delete_skill(skill_id: str, db: Session = Depends(get_db)):
    try:
        skills = crud.delete_skill(skill_id, db=db)
    except ItemNotFoundException:
        raise HTTPException(404, f"no skill found with id {skill_id}")
        
    return {"details": f"skill {skill_id} successfully deltetd"}

@router.get("/", response_model=List[SkillSchema])
def get_skills(db: Session = Depends(get_db)):
    skills = crud.get_skills(db=db)
    
    return [SkillSchema.parse_orm(skill) for skill in skills]