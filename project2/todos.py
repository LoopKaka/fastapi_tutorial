from fastapi import Body, FastAPI, HTTPException
from TodoModel import Todo
from TodoRequest import TodoRequest
from TodoResponse import TodoResponse

app = FastAPI(
    title="LoopKaka's FastAPI Tutorial",
    version="0.0.1",
    description="This is chater 2 and project 2"
)

TODOS = [
    Todo(1, "Task 1", "My Task 1", False, 1),
    Todo(2, "Task 2", "My Task 2", False, 1),
    Todo(3, "Task 3", "My Task 3", False, 1),
    Todo(4, "Task 4", "My Task 4", False, 1)
]

@app.get("/todos/all", response_model=list[TodoResponse], status_code=200)
async def get_all():
    return TODOS

@app.get("/todo/get", response_model=list[TodoResponse], status_code=200)
async def get_by_priority(priority: int):
    result = []

    for todo in TODOS:
        if todo.priority == priority:
            result.append(todo)

    return result

@app.post("/todos/create", response_model=TodoResponse, status_code=201)
async def create_todo(todo: TodoRequest):
    t = Todo(**todo.dict())
    TODOS.append(get_todo_id(t))
    return t

@app.put("/todos/update", response_model=TodoResponse, status_code=201)
async def update_todo(todo: TodoRequest):
    t = Todo(**todo.dict())
    not_found = True
    for index in range(len(TODOS)):
        if TODOS[index].id == t.id:
            TODOS[index] = t
            return t

    if not_found == True:
        raise HTTPException(status_code=400, detail="Id not found") 

        

@app.delete("/todos/remove/{id}", status_code=204)
async def delete_todo(id: int):
    not_found = True
    for index in range(len(TODOS)):
        if TODOS[index].id == id:
            TODOS.pop(index)
            return
    if not_found == True:
        raise HTTPException(status_code=400, detail="Id not found")  

        


def get_todo_id(todo):
    if len(TODOS) == 0:
        todo.id = 1
    else:
        todo.id = TODOS[-1].id + 1
    return todo

