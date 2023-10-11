from fastapi import APIRouter, status, HTTPException
from app.db.models.user import User
from app.db.client import db_client
from app.db.schemas.user import user_schema, users_schema
from bson import ObjectId

router = APIRouter()


users_db = []

newuser = User(
    username="nops",
    email="ricpascual29999@gmail.com")


@router.get("/usersdb", response_model=list[User])
async def users():
    return users_schema(db_client.local.users.find())


@router.get("/userdb/{id}")
async def user(id: str):
    return search_user("_id", ObjectId(id))


@router.get("/userdb/")
async def user(id: str):
    return search_user("_id", ObjectId(id))


@router.post("/userdb/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    if type(search_user("email", user.email)) == User:
        print(user.email)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="el usuario ya existe")

    print(newuser)
    user_dict = dict(user)
    del user_dict["id"]
    id = db_client.local.users.insert_one(user_dict).inserted_id
    new_user = user_schema(db_client.local.users.find_one({"_id": id}))
    return User(**new_user)


@router.put("/userdb", response_model=User)
async def user(user: User):
    user_dic = dict(user)
    del user_dic["id"]

    try:
        found = db_client.local.users.find_one_and_replace(
            {"_id": ObjectId(user.id)}, user_dic)
    except:
        return {"error": "usuario no encontrado"}

    return search_user("_id", ObjectId(user.id))


@router.delete("/userdb/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):
    found = db_client.local.users.find_one_and_delete({"_id": ObjectId(id)})
    if not found:
        return {"error": "no se ha eliminaod el usiario"}


def search_user(field: str, key):
    try:
        user = user_schema(db_client.local.users.find_one({field: key}))
        return User(**user)
    except:
        return {"error": "no se aha encontrado un usuario"}
