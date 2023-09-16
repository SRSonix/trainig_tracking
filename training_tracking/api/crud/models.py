#from __future__ import annotations
from typing import List

from sqlalchemy import Table, Column, ForeignKey, VARCHAR, Text, Enum, TIMESTAMP, ForeignKeyConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column

from training_tracking.api.crud.utils import Base

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
    
    id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True, nullable=False)
    description = mapped_column(Text, nullable=True)
    excercises: Mapped[List["Exercise"]] = relationship(
        secondary=exercise_skill, back_populates="skills"
    )
    
class Exercise(Base):
    __tablename__ = "exercises"
    
    id = Column(VARCHAR(32), primary_key=True, nullable=False)
    variation = Column(VARCHAR(32), primary_key=True, nullable=False)
    description = Column(Text, nullable=True)
    skills: Mapped[List["Skill"]] = relationship(
        secondary=exercise_skill, back_populates="excercises"
    )
