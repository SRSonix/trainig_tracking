from __future__ import annotations
from typing import Optional, List, Any

from pydantic import BaseModel, Field, validator

from api.crud.models import Skill as SkillCrud, Exercise as ExerciseCrud, DOMAIN as Domain


class Skill(BaseModel):
    id: str = Field(...)
    description: str = Field(default="")
    excercises: List[Any] = Field(default=[]) # we cannot use List[Exercise], because FastAPI does not deal with Forward-references

    @staticmethod
    def parse_orm(skill: SkillCrud, parse_children: bool = True) -> Skill:
        skill =  Skill(id=skill.id, description=skill.description, excercises=[Exercise.parse_orm(e, parse_children=False) for e in skill.excercises if parse_children])
        
        return skill
    
    @validator("excercises")
    def parse_excercises(cls, excercises):
        excercises = [Exercise.parse_obj(excercise) for excercise in excercises]
        return excercises
    

class Exercise(BaseModel):
    id: str = Field(...)
    variation: str = Field(...)
    domain: Domain = Field(...)
    description: Optional[str] = Field(default=None)
    skills: List[Any] = Field(default=[]) # we cannot use List[Skill], to be consistent with Skill
    
    @staticmethod
    def parse_orm(excercise: ExerciseCrud, parse_children: bool=True) -> Exercise:
        return Exercise(id=excercise.id, variation=excercise.variation, domain=excercise.domain, description=excercise.description, skills=[Skill.parse_orm(s, parse_children=False) for s in excercise.skills if parse_children])
        
    @validator("skills")
    def parse_skills(cls, skills):
        skills = [Skill.parse_obj(skill) for skill in skills]
        return skills
            