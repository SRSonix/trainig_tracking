from typing import List, Optional
from abc import ABC, abstractmethod

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from training_tracking.api.crud.models import Skill, Exercise
from training_tracking.api.schemas import Skill as SkillSchema, Exercise as ExerciseSchema
from training_tracking.api.crud.utils import UniqueIdException, ItemNotFoundException, DependentItemNotFoundException


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
        
        skill_db.excercises = []
        for exercise in skill.excercise_ids:
            try: 
                exercise = exercise_crud.get_one(exercise.id, exercise.variation)
            except ItemNotFoundException as e:
                raise DependentItemNotFoundException(e.message, e.class_str, e.id)
            skill_db.excercises.append(exercise)
                
        return skill_db
    
    @staticmethod
    def _apply_filter(query, id: Optional[str] = None):
        if id is not None:
            query = query.filter(Skill.id == id)
        return query
        
    def get(self, id: Optional[str] = None) -> List[Skill]:
        query = self.db.query(Skill)
        query = self._apply_filter(query, id=id)
        
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
        skill = self.get_one(id)
            
        self.db.delete(skill)
        self.db.commit()
        
    
class ExerciseCrud(Crud):
    def __init__(self, db: Session) -> None:
        self.db = db
   
    def to_orm(self, exercise: ExerciseSchema) -> Exercise:
        exercise_db = Exercise(id=exercise.id, variation=exercise.variation, description=exercise.description)
        skill_crud = SkillCrud(self.db)
        
        skill_crud.skills=[]
        for id in exercise.skill_ids:
            try: 
                skill = skill_crud.get_one(id=id)
            except ItemNotFoundException as e:
                raise DependentItemNotFoundException(e.message, e.class_str, e.id)

            exercise_db.skills.append(skill)
        
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
        exercise = self.get_one(id=id, variation=variation)
            
        self.db.delete(exercise)
        self.db.commit()