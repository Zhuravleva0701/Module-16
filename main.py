from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def welcome() -> str:
    return 'Главная страница'


@app.get('/user/admin')
async def welcome() -> str:
    return "Вы вошли как администратор"


@app.get('/user/{user_id}')
async def welcome(user_id: str) -> str:
    return f'Вы вошли как пользователь № {user_id}'


@app.get('/user')
async def welcome(username: str, age: int):
    return f'Информация о пользователе. Имя: {username}, Возраст: {age}'
