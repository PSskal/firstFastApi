from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter()


# etidad user


class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int


users_db = [User(id=1, name="richard", surname="huallpa", url="http://localhost:", age=21),
            User(id=2, name="pascual", surname="yapo",
                 url="http://localhe:", age=20),
            User(id=3, name="zinedine", surname="aroostigue",
                 url="http://localhost:.com", age=23),
            User(id=4, name="liz", surname="condori",
                 url="http://localhost:.es", age=17),
            User(id=5, name="elaina", surname="supho", url="http://localhost:", age=17)]


@router.get("/users")
async def users():
    return users_db


@router.get("/user/{id}")
async def user(id: int):
    return search_users(id)


@router.get("/user/")
async def user(id: int):
    return search_users(id)


def search_users(id):
    users = list(filter(lambda user: user.id == id, users_db))
    try:
        return users[0]
    except:
        return {"message": "error"}


@router.post("/user/")
async def user(user: User):
    if type(search_users(user.id)) == User:
        return {"error": "el usiario ya extiste"}
    else:
        users_db.append(user)


@router.put("/user/")
async def user(user: User):
    found = False
    for index, saved_user in enumerate(users_db):
        if saved_user.id == user.id:
            users_db[index] = user
            found = True
    if not found:
        return {"error": "usuario no encontrado"}


@router.delete("/user/{id}/")
async def user(id: int):
    found = False
    for index, saved_user in enumerate(users_db):
        if saved_user.id == id:
            del users_db[index]
            found = True
    if not found:
        return {"error": "no se ha eliminaod el usiario"}
