from __future__ import annotations
from typing import Optional

from pydantic import BaseModel, Field

from api.crud.models import Skill as SkillCrud


class Skill(BaseModel):
    id: str = Field(...)
    description: str = Field(default="")

    @staticmethod
    def parse_orm(skill: SkillCrud) -> Skill:
        return Skill(id=skill.id, description=skill.description)
