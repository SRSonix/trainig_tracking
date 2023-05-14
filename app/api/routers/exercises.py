from typing import List

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from api.schemas import Exercise
from api.crud.crud import ExerciseCrud
from api.crud.utils import UniqueIdException, ItemNotFoundException
from api.utils import get_db 

router = APIRouter(
    prefix="/exercises",
    tags=["exercises"],
    responses={409: {"description": "Key not unique."},
        404: {"description": "Not found."}},
)

@router.get("/", response_model=List[Exercise])
def get_excercises(db: Session = Depends(get_db)):
    exercises = ExerciseCrud(db=db).get()
    
    return [Exercise.parse_orm(e) for e in exercises]
    
@router.post("/", response_model=Exercise)
def insert_excercice(skill: Exercise, db: Session = Depends(get_db)):
    try:
        db_skill = ExerciseCrud(db=db).create(skill)
    except ItemNotFoundException as e:
        raise HTTPException(422, e.message)
    except UniqueIdException as e:
        raise HTTPException(409, e.message)
    return Exercise.parse_orm(db_skill)

@router.put("/{id}/{variation}", response_model=Exercise)
def replace_skill(id: str, variation:str, exercise: Exercise, db: Session = Depends(get_db)):
    if (id != exercise.id) or (variation != exercise.variation):
        raise HTTPException(422, "Exercise id and variation must be correspond to the one in the URL.")
    
    try:
        exercise = ExerciseCrud(db=db).replace(exercise=exercise)
    except ItemNotFoundException as e:
        raise HTTPException(404, e.message)
        
    return Exercise.parse_orm(exercise)

@router.delete("/{id}/{variation}")
def delete_skill(id: str, variation:str, db: Session = Depends(get_db)):
    try:
        ExerciseCrud(db=db).delete(id, variation)
    except ItemNotFoundException as e:
        raise HTTPException(404, e.message)
        
    return {"details": f"Exercise {id}/{variation} successfully deltetd."}
