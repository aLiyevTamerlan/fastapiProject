from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session
from models import Todos
from schema import TodoList

from database import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/all/")
async def read_all(db: db_dependency):
    return db.query(Todos).all()

@router.get("/todo/{todo_id}")
async def get_item(db: db_dependency, todo_id: int):
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    return todo

@router.post("/todo/create/")
async def create_item(db: db_dependency, list_body: TodoList):

    todo_model = Todos(**list_body.dict())
    db.add(todo_model)
    db.commit()
    return list_body

@router.put("/todo/{todo_id}/", status_code=status.HTTP_200_OK)
async def update_todo( 
                       db: db_dependency,
                       todo_request:TodoList,
                       todo_id:int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id==todo_id).first()
    
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Not found")
    
    todo_model.title = todo_request.title
    
    todo_model.complete = todo_request.complete
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    db.add(todo_model)
    db.commit()
    return todo_request
