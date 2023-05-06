from typing import List, Optional

from sqlalchemy import delete
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from api.crud.models import Skill
from api.schemas import Skill as SkillSChema
from api.crud.utils import UniqueIdException, ItemNotFoundException


def create_skill(skill: SkillSChema, db: Session) -> Skill:
    db_skill = Skill(**skill.dict())
   
    db.add(db_skill)
    try:
        db.commit()    
    except IntegrityError:
        raise UniqueIdException("skill id must be unique")
    
    db.refresh(db_skill)
    return db_skill

def get_skill(skill_id: str, db:Session) -> Optional[Skill]:
    return db.query(Skill).filter(Skill.id == skill_id).first()

def get_skills(db:Session) -> List[Skill]:
    query = db.query(Skill)
    
    return query.all()
    
def delete_skill(skill_id: str, db: Session) -> bool:
    skill = get_skill(skill_id, db=db)
    if skill is None:
        raise ItemNotFoundException(f"No skill with id {skill_id}")
        
    db.delete(skill)
    db.commit()
    
    return True