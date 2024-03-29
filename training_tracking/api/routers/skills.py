from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from training_tracking.api.crud.crud import SkillCrud
from training_tracking.api.crud.utils import UniqueIdException, ItemNotFoundException, DependentItemNotFoundException
from training_tracking.api.schemas import Skill, SkillAttributes
from training_tracking.api.utils import get_db

router = APIRouter(
    prefix="/skills",
    tags=["skills"],
    responses={409: {"description": "Key not unique"},
        404: {"description": "Not found"}},
)

@router.get("/", response_model=List[Skill])
def get_skills(db: Session = Depends(get_db), id: Optional[str] = None):
    skills = SkillCrud(db=db).get(id=id)
    
    return [Skill.validate_orm(skill) for skill in skills]

    
@router.post("/", response_model=Skill)
def insert_skill(skill: Skill, db: Session = Depends(get_db)):
    try:
        db_skill = SkillCrud(db=db).create(skill)
    except ItemNotFoundException as e:
        raise HTTPException(422, e.message)
    except UniqueIdException as e:
        raise HTTPException(409, e.message)
    return Skill.validate_orm(db_skill)


@router.put("/{id}", response_model=Skill)
def replace_skill(id: str, attributes: SkillAttributes, db: Session = Depends(get_db)):
    skill = Skill(id=id, **attributes.model_dump())

    try:
        skill = SkillCrud(db=db).replace(skill=skill)
    except ItemNotFoundException as e:
        raise HTTPException(404, e.message)
    except DependentItemNotFoundException as e:
        raise HTTPException(422, e.message)
        
    return Skill.validate_orm(skill)


@router.delete("/{id}")
def delete_skill(id: str, db: Session = Depends(get_db)):
    try:
        SkillCrud(db=db).delete(id)
    except ItemNotFoundException as e:
        raise HTTPException(404, e.message)
        
    return {"details": f"skill {id} successfully deltetd"}
