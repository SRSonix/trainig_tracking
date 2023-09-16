from typing import List

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from training_tracking.api.schemas import Exercise, ExerciseAttributes
from training_tracking.api.crud.crud import ExerciseCrud
from training_tracking.api.crud.utils import UniqueIdException, ItemNotFoundException, DependentItemNotFoundException
from training_tracking.api.utils import get_db 

router = APIRouter(
    prefix="/exercises",
    tags=["exercises"],
    responses={409: {"description": "Key not unique."},
        404: {"description": "Not found."}},
)

@router.get("/", response_model=List[Exercise])
def get_excercises(db: Session = Depends(get_db)):
    exercises = ExerciseCrud(db=db).get()
    
    return [Exercise.validate_orm(e) for e in exercises]
    
@router.post("/", response_model=Exercise)
def insert_excercice(skill: Exercise, db: Session = Depends(get_db)):
    try:
        db_skill = ExerciseCrud(db=db).create(skill)
    except ItemNotFoundException as e:
        raise HTTPException(422, e.message)
    except UniqueIdException as e:
        raise HTTPException(409, e.message)
    return Exercise.validate_orm(db_skill)

@router.put("/{id}/{variation}", response_model=Exercise)
def replace_skill(id: str, variation:str, attributes: ExerciseAttributes, db: Session = Depends(get_db)):
    exercise = Exercise(id=id, variation=variation, **attributes.model_dump())
    
    try:
        exercise = ExerciseCrud(db=db).replace(exercise=exercise)
    except ItemNotFoundException as e:
        raise HTTPException(404, e.message)
    except DependentItemNotFoundException as e:
        raise HTTPException(422, e.message)
        
    return Exercise.validate_orm(exercise)

@router.delete("/{id}/{variation}")
def delete_skill(id: str, variation:str, db: Session = Depends(get_db)):
    try:
        ExerciseCrud(db=db).delete(id, variation)
    except ItemNotFoundException as e:
        raise HTTPException(404, e.message)
        
    return {"details": f"Exercise {id}/{variation} successfully deltetd."}
