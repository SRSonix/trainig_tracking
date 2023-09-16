from __future__ import annotations
from typing import Optional, List, Any

import enum
from pydantic import BaseModel, Field, validator, Extra, ValidationError

class Domain(enum.Enum):
    gym='gym'
    running='running'
    drums='drums'
    guitar='guitar'

class Skill(BaseModel):
    id: str = Field(...)
    domain: Domain = Field(...)
    description: str = Field(default="")
    excercises: List[Any] = Field(default=[]) # we cannot use List[Exercise], because FastAPI does not deal with Forward-references

    @validator("excercises")
    def parse_excercises(cls, excercises):
        excercises = [Exercise.parse_obj(excercise) for excercise in excercises]
        return excercises
    
    @validator("id")
    def id_is_not_empty(cls, id):
        if id == "":
            raise ValueError("Id cannot be empty.")
        return id
    
    class Config:
        extra = Extra.forbid
    

class Exercise(BaseModel):
    id: str = Field(...)
    variation: str = Field(...)
    domain: Domain = Field(...)
    description: Optional[str] = Field(default=None)
    skills: List[Any] = Field(default=[]) # we cannot use List[Skill], to be consistent with Skill
    
    @validator("id")
    def id_is_not_empty(cls, id):
        if id == "":
            raise ValidationError("Id cannot be empty.")
        return id
    
    @validator("variation")
    def variation_is_not_empty(cls, variation):
        if variation == "":
            raise ValidationError("Variation cannot be empty.")
        return variation
    
    @validator("skills")
    def parse_skills(cls, skills):
        skills = [Skill.parse_obj(skill) for skill in skills]
        return skills
            
    class Config:
        extra = Extra.forbid
