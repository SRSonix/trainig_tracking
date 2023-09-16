from __future__ import annotations

from shared_models.schemas import Skill, Exercise

from api.crud.models import Skill as SkillCrud, Exercise as ExerciseCrud


class Skill(Skill):
    @staticmethod
    def parse_orm(skill: SkillCrud, parse_children: bool = True) -> Skill:
        skill =  Skill(id=skill.id, description=skill.description, domain=skill.domain, excercises=[Exercise.parse_orm(e, parse_children=False) for e in skill.excercises if parse_children])
        
        return skill
        

class Exercise(Exercise):
    @staticmethod
    def parse_orm(excercise: ExerciseCrud, parse_children: bool=True) -> Exercise:
        return Exercise(id=excercise.id, variation=excercise.variation, domain=excercise.domain, description=excercise.description, skills=[Skill.parse_orm(s, parse_children=False) for s in excercise.skills if parse_children])
