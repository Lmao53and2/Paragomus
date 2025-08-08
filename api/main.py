from fastapi import Path
from storage.task_db import get_all_tasks
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class TaskIn(BaseModel):
    title: str
    description: str = ""
    due_date: str = None
    priority: str = "normal"
    status: str = "todo"
    project_id: str = None

@app.get("/tasks")
def api_get_all_tasks():
    return get_all_tasks()


@app.put("/tasks/{task_id}")
def api_update_task(task_id: str, task: TaskIn):
    return update_task(task_id, task.dict())

@app.delete("/tasks/{task_id}")
def api_delete_task(task_id: str):
    return delete_task(task_id)
