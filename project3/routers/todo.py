from typing import Annotated
from fastapi import Depends, HTTPException, Path, Query, status, APIRouter
from sqlmodel import select
from models.Todo import Todo
from database.db import SessionDependency
from request_model.TodoRequest import TodoRequest
from response_model.TodoResponse import TodoResponse
from utility import validate_token

router = APIRouter(
    prefix="/todo",
    tags=["Todo"]
)

auth_user_dependency = Annotated[dict, Depends(validate_token)]

@router.post("/create", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(todoReq: TodoRequest, user: auth_user_dependency, session: SessionDependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to authorize")
    
    todo_data = todoReq.model_dump()
    todo_data['user_id'] = user.get('id')
    todo = Todo.model_validate(todo_data)
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

@router.get("/all", response_model=list[TodoResponse])
async def get_all(user: auth_user_dependency, session: SessionDependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to authorize")
    
    query = select(Todo).where(Todo.user_id == user.get("id"))
    result = session.exec(query).all()
    return result

@router.get("/priority", response_model=list[TodoResponse])
async def get_todo_by_priority(user: auth_user_dependency, session: SessionDependency, priority: int = Query(ge=1, le=5)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to authorize")
    
    userId = user.get("id")

    query = select(Todo).where(Todo.priority == priority, Todo.user_id == userId)
    result = session.exec(query).all()
    return result

@router.get("/{id}", response_model=TodoResponse)
async def get_todo_by_id(user: auth_user_dependency, session: SessionDependency, id: int = Path(ge=1)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to authorize")
    
    userId = user.get("id")
    todo = session.exec(select(Todo).where(Todo.id == id, Todo.user_id == userId)).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Id Not Found")
    return todo

@router.put("/{id}", response_model=TodoResponse)
async def update_todo(todoReq: TodoRequest, user: auth_user_dependency, session: SessionDependency, id: int = Path(ge=1)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to authorize")
    
    userId = user.get("id")
    todo = session.exec(select(Todo).where(Todo.id == id, Todo.user_id == userId)).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Id Not Found")
    
    todo.title = todoReq.title
    todo.description = todoReq.description
    todo.priority = todoReq.priority
    todo.is_completed = todoReq.is_completed
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo_by_id(user: auth_user_dependency, session: SessionDependency, id: int = Path(ge=1)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to authorize")
    
    userId = user.get("id")
    todo = session.exec(select(Todo).where(Todo.id == id, Todo.user_id == userId)).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Id Not Found")
    
    session.delete(todo)
    session.commit()
    return

