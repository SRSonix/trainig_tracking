from typing import List, Optional
from abc import ABC, abstractmethod

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from api.crud.models import Skill, Exercise
from api.schemas import Skill as SkillSchema, Exercise as ExerciseSchema
from api.crud.utils import UniqueIdException, ItemNotFoundException


class Crud(ABC):
    def __init__(self, db: Session) -> None:
        self.db = db
        
    @abstractmethod
    def to_orm(self, **kwargs):
        raise NotImplementedError
    
    @abstractmethod
    def get(self, **kwargs):
        raise NotImplementedError
    
    @abstractmethod
    def get_one(self, **kwargs):
        raise NotImplementedError
    
    @abstractmethod
    def create(self, **kwargs):
        raise NotImplementedError
    
    @abstractmethod
    def replace(self, **kwargs):
        raise NotImplementedError
    
    @abstractmethod
    def delete(self, **kwargs):
        raise NotImplementedError


class SkillCrud(Crud):
    def to_orm(self, skill: SkillSchema) -> Exercise:
        skill_db = Skill(id=skill.id, description=skill.description)
        exercise_crud = ExerciseCrud(self.db)
        
        for exercise in skill.excercises:
            skill_db.excercises.append(exercise_crud.get_one(exercise.id, exercise.variation))
        
        return skill_db
    
    def get(self) -> List[Skill]:
        query = self.db.query(Skill)
        
        return query.all()
    
    def get_one(self, id: str) -> Optional[Skill]:
        skill = self.db.query(Skill).filter(Skill.id == id).first()
        if skill is None:
            raise ItemNotFoundException(f"No skill with id {id}.", "Skill", id)
        return skill

    def create(self, skill: SkillSchema) -> Skill:
        db_skill = self.to_orm(skill)
    
        self.db.add(db_skill)
        try:
            self.db.commit()    
        except IntegrityError:
            raise UniqueIdException("Skill id must be unique.", "Skill", id)
        
        self.db.refresh(db_skill)
        return db_skill
    
    def replace(self, skill: SkillSchema) -> Skill:
        skill = self.to_orm(skill)
        skill_db = self.get_one(id=skill.id)
        
        for key, value in skill.__dict__.items():
            if key[0] != "_":
                setattr(skill_db, key, value)
        
        self.db.commit()
        return skill_db
        
    def delete(self, id: str) -> None:
        skill = self.get_skill(id)
            
        self.db.delete(skill)
        self.db.commit()
        
    
class ExerciseCrud(Crud):
    def __init__(self, db: Session) -> None:
        self.db = db
   
    def to_orm(self, exercise: ExerciseSchema) -> Exercise:
        exercise_db = Exercise(id=exercise.id, variation=exercise.variation, domain=exercise.domain, description=exercise.description)
        skill_crud = SkillCrud(self.db)
        
        for skill in exercise.skills:
            exercise_db.skills.append(skill_crud.get_one(skill.id))
        
        return exercise_db

    def get(self) -> List[Exercise]:
        query = self.db.query(Exercise)
        
        return query.all()

    def get_one(self, id: str, variation: str) -> Optional[Skill]:
        exercise = self.db.query(Exercise).filter((Exercise.id == id) & (Exercise.variation == variation)).first()
        if exercise is None:
            raise ItemNotFoundException(f"No exercise with id={id} and variation={variation}.", "Exercise", f"{id}/{variation}")
        return exercise
    
    def create(self, exercise: ExerciseSchema) -> Exercise:
        db_exercise = self.to_orm(exercise)
    
        self.db.add(db_exercise)
        try:
            self.db.commit()    
        except IntegrityError:
            raise UniqueIdException("Exercise id/variation must be unique.", "Exercise", f"{exercise.id}/{exercise.variation}")
        
        self.db.refresh(db_exercise)
        return db_exercise
    
    def replace(self, exercise: ExerciseSchema) -> Skill:
        exercise = self.to_orm(exercise)
        exercise_db = self.get_one(id=exercise.id, variation=exercise.variation)
        
        for key, value in exercise.__dict__.items():
            if key[0] != "_":
                setattr(exercise_db, key, value)
        
        self.db.commit()
        return exercise_db
    
    def delete(self, id: str, variation) -> None:
        exercise = self.get_exercise(id=id, variation=variation)
            
        self.db.delete(exercise)
        self.db.commit()