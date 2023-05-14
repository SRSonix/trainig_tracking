from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.crud.crud import SkillCrud
from api.crud.utils import UniqueIdException, ItemNotFoundException
from api.schemas import Skill
from api.utils import get_db

router = APIRouter(
    prefix="/skills",
    tags=["skills"],
    responses={409: {"description": "Key not unique"},
        404: {"description": "Not found"}},
)

@router.get("/", response_model=List[Skill])
def get_skills(db: Session = Depends(get_db)):
    skills = SkillCrud(db=db).get()
    
    return [Skill.parse_orm(skill) for skill in skills]
    
@router.post("/", response_model=Skill)
def insert_skill(skill: Skill, db: Session = Depends(get_db)):
    try:
        db_skill = SkillCrud(db=db).create(skill)
    except ItemNotFoundException as e:
        raise HTTPException(422, e.message)
    except UniqueIdException as e:
        raise HTTPException(409, e.message)
    return Skill.parse_orm(db_skill)

@router.put("/{id}", response_model=Skill)
def replace_skill(id: str, skill: Skill, db: Session = Depends(get_db)):
    if id != skill.id:
        raise HTTPException(422, "Skill id must be correspond to the one in the URL.")
    
    try:
        skill = SkillCrud(db=db).replace(skill=skill)
    except ItemNotFoundException as e:
        raise HTTPException(404, e.message)
        
    return Skill.parse_orm(skill)


@router.delete("/{id}")
def delete_skill(id: str, db: Session = Depends(get_db)):
    try:
        SkillCrud(db=db).delete(id)
    except ItemNotFoundException as e:
        raise HTTPException(404, e.message)
        
    return {"details": f"skill {id} successfully deltetd"}
