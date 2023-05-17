from pydantic import BaseModel

class TodoList(BaseModel):
    id: int
    title: str
    description: str
    priority: int
    complete: bool
    class Config:
        orm_mod = True



