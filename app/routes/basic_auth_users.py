from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool


class UserDB(User):
    password: str


user_db = {
    "mourodev": {
        "username": "mourodev",
        "full_name": "richardLucas",
        "email": "ricapscial29@gmail.com",
        "disabled": False,
        "password": "123abc"
    },
    "mourodev2": {
        "username": "mourodev2",
        "full_name": "richardLucas2",
        "email": "ricapscial29@gmail.com2",
        "disabled": True,
        "password": "123abc"
    }
}


def search_user(username: str):
    if username in user_db:
        return UserDB(**user_db[username])


async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="creedenciales invalidad", headers={"WWW-Authenticate": "Bearer"})
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")
    return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    userdb = user_db.get(form.username)

    if not userdb:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    print(user_db["mourodev2"])
    user = search_user(form.username)

    if not form.password == user.password:
        raise HTTPException(
            status_code=400, detail="La contraseña no es correcta")

    return {"access_token": user.username, "token_type": "Bearer"}


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
