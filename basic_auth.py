import hashlib
import json
from random import choices
from string import ascii_letters

from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from pydantic import BaseModel

router = APIRouter(tags=["basic"], prefix="/basic")
get_credentials = HTTPBasic()


def get_hash(password: str, salt: str) -> str:
    password_hash = hashlib.sha256(password.encode()+salt.encode()).hexdigest()
    return password_hash




@router.get("/test_auth", status_code=status.HTTP_200_OK)
async def test_auth(credentials: HTTPBasicCredentials=Depends(get_credentials)):
    with open("db.json") as f:
        db = json.load(f)
    for user in db:
        if credentials.username == user["nickname"]:
            print(f"{"совпали имена"}, {credentials.username}, {user["nickname"]}")
            basic_hash = get_hash(credentials.password, user["password_salt"])
            # basic_hash_2 = get_hash(credentials.password, user["password_salt"])
            basic_hash_amount: str = basic_hash
            basic_hash_3 = user["password_hash"]
            # basic_hash_4 = basic_hash_3.replace('""', '')
            print(f"{"basic_hash_amount"} - {basic_hash_amount} {"basic_hash_3"} - {basic_hash_3}")
            # if (get_hash(credentials.password, user["password_salt"])+user["password_salt"])== user["password_hash"]+user["password_salt"]:
            if basic_hash_amount == basic_hash_3:
                print("совпали пароли")
                print("Добро пожаловать в систему")
                return user["data"]
            else:
                print(f"{"Пароли не совпали"}")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не авторизован")


@router.get("/data", status_code=status.HTTP_200_OK)
async def get_data(nickname: str) -> str:
    with open("db.json") as f:
        db =json.load(f)
    for user in db:
        if nickname == user["nickname"]:
            print(f"Hello, {nickname}")
            return user["data"]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")


class CreateUserSchema(BaseModel):
    nickname: str
    password: str
    data: str


class ReadUserSchema(BaseModel):  # password и solt не возвращаем при запросе
    nickname: str
    data: str


@router.post("/register", status_code=status.HTTP_204_NO_CONTENT)
async def register(user: CreateUserSchema):
    with open("db.json") as f:
        db =json.load(f)
    for users in db:
        if user.nickname == users["nickname"]:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Такой никнэйм уже есть")
    salt = "".join(choices(ascii_letters, k=16))
    user_dict = {
        "nickname": user.nickname,
        "password_hash": get_hash(user.password, salt),
        "password_salt": salt,
        "data": user.data,
    }
    db.append(user_dict)
    with open("db.json", "w") as f:
        json.dump(db, f, indent=4)
    


@router.get("/get_users")
async def get_users() -> list[ReadUserSchema]:
    with open("db.json") as f:
        db =json.load(f)
    return db






