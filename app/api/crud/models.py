#from __future__ import annotations
from typing import List

import enum
from sqlalchemy import Table, Column, ForeignKey, VARCHAR, Text, Enum, TIMESTAMP, ForeignKeyConstraint
from sqlalchemy.orm import relationship, Mapped

from api.crud.utils import Base

class DOMAIN(enum.Enum):
    gym='gym'
    running='running'
    drums='drums'
    guitar='guitar'

exercise_skill = Table(
    "exercise_skill",
    Base.metadata,
    Column("exercise_id", VARCHAR(32), primary_key=True),
    Column("variation", VARCHAR(32), primary_key=True),
    Column("skill_id", VARCHAR(32), ForeignKey("skills.id"), primary_key=True),
    ForeignKeyConstraint(("exercise_id", "variation"),("exercises.id", "exercises.variation"))
)

class Skill(Base):
    __tablename__ = "skills"
    
    id = Column(VARCHAR(32), primary_key=True, nullable=False)
    description = Column(Text, nullable=True)
    excercises: Mapped[List["Exercise"]] = relationship(
        secondary=exercise_skill, back_populates="skills"
    )
    
class Exercise(Base):
    __tablename__ = "exercises"
    
    id = Column(VARCHAR(32), primary_key=True, nullable=False)
    variation = Column(VARCHAR(32), primary_key=True, nullable=False)
    domain = Column(Enum(DOMAIN), nullable=False)
    description = Column(Text, nullable=True)
    skills: Mapped[List["Skill"]] = relationship(
        secondary=exercise_skill, back_populates="excercises"
    )

class Executaion(Base):
    __tablename__ = "executions"

    id = Column(VARCHAR(32), primary_key=True, nullable=False)
    exercise_id = Column(ForeignKey("exercises.id"), primary_key=True, nullable=False)
    variation = Column(ForeignKey("exercises.id"), primary_key=True, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)
    executed_at = Column(TIMESTAMP, nullable=False)
    difficulty = Column(VARCHAR(128), nullable=False)
