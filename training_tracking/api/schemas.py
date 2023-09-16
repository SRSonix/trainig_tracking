from __future__ import annotations
from typing import Optional, List, Annotated

import enum
from pydantic import field_validator, ConfigDict, BaseModel, Field, ValidationError, StringConstraints

from training_tracking.api.crud.models import Skill as SkillORM, Exercise as ExerciseORM

class ExerciseId(BaseModel):
    id: Annotated[str, StringConstraints(min_length=1)]  = Field(...)
    variation: Annotated[str, StringConstraints(min_length=1)] = Field(...)
    model_config = ConfigDict(extra="forbid")
    
    def validate_orm(excercise: ExerciseId | ExerciseORM):
        return ExerciseId(
            id=excercise.id,
            variation=excercise.variation
        )

class ExerciseAttributes(BaseModel):
    description: Optional[str] = Field(default=None)
    skill_ids: List[str] = Field(default=[])
    model_config = ConfigDict(extra="forbid")
    
    
class Exercise(ExerciseId, ExerciseAttributes):
    @staticmethod
    def validate_orm(excercise: ExerciseORM,) -> Exercise:
        return Exercise(
            id=excercise.id, 
            variation=excercise.variation, 
            description=excercise.description, 
            skill_ids=[s.id for s in excercise.skills]
        )


class SkillId(BaseModel):
    id: Annotated[str, StringConstraints(min_length=1)]  = Field(...)
    
    
class SkillAttributes(BaseModel):
    description: str = Field(default="")
    excercise_ids: List[ExerciseId] = Field(default=[])
    model_config = ConfigDict(extra="forbid")
    

class Skill(SkillId, SkillAttributes):
    @staticmethod
    def validate_orm(skill: SkillORM) -> Skill:
        skill =  Skill(
            id=skill.id, 
            description=skill.description, 
            excercise_ids=[ExerciseId.validate_orm(e) for e in skill.excercises]
        )
        
        return skill