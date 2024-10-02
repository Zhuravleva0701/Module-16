from fastapi import FastAPI, Path, HTTPException, Request
from pydantic import BaseModel
from typing import Annotated
from typing import List
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory='templates')
users = []


class User(BaseModel):
    id: int = None
    username: str
    age: int


@app.get('/')
async def get_main_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'Users': users})


@app.get('/users/{user_id}')
async def get_users(request: Request, user_id: int) -> HTMLResponse:
    try:
        for user in users:
            if user.id == user_id:
                return templates.TemplateResponse('users.html', {'request': request, 'users': user})
    except ValueError:
        raise HTTPException(status_code=404, detail='User was not found')


@app.post('/user/{username}/{age}')
async def post_user(username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser')]
                    , age: Annotated[int, Path(ge=18, le=120, description='Enter age', example='24')]) -> User:
    next_id = len(users) + 1
    # user_id = str(int(max(users, key=int)) + 1)
    user = User(id=next_id, username=username, age=age)
    users.append(user)
    return user


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: int, username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser')]
                      , age: Annotated[int, Path(ge=18, le=120, description='Enter age', example='24')]) -> User:
    try:
        for user in users:
            if user.id == user_id:
                user.username = username
                user.age = age
                return user
    except ValueError:
        raise HTTPException(status_code=404, detail='User was not found')


@app.delete('/user/{user_id}')
async def delete_user(user_id: int) -> None:
    try:
        for user in users:
            if user.id == user_id:
                return users.remove(user_id)
    except ValueError:
        raise HTTPException(status_code=404, detail='User was not found')

