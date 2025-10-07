import hashlib
import json
from random import choices
from string import ascii_letters
from typing import Any, Coroutine

from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBasicCredentials
from pydantic import BaseModel

from basic_auth import get_credentials, get_hash

router = APIRouter(tags=["basic_2"], prefix="/basic_2")





class CreateUserSchema(BaseModel):
    nickname: str
    password: str
    data: str


class ReadUserSchema(BaseModel):
    id: int
    nickname: str
    data: str

class UserRepository:
    def get_users(self) -> list[ReadUserSchema]:  # вывести всех пользователей
        with open("db_2.json") as f:
            db = json.load(f)
        return db

    def get_user(self, nickname: str, password: str) -> ReadUserSchema:
        users = self.get_users()
        for user in users:
            if nickname == user["nickname"]:
                print("Имена совпали")
                if get_hash(password, user["password_salt"]) == user["password_hash"]:
                    print(f"{"Поздравляю! Вы вошли в систему как "} - {nickname}")
                    return user
                else:
                    print("Пароли не совпали")
        print("Совпадений нет")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не найден")

    def get_user_by_id(self, user_id: int) -> ReadUserSchema:
        with open("db_2.json") as f:
            db = json.load(f)
        for user in db:
            if user_id == user["id"]:
                return user
        return None

    def get_hash(self, password:str, salt: str) -> str:
        password_hash = hashlib.sha256(password.encode()+salt.encode()).hexdigest()
        return password_hash

    def create_user(self, user: CreateUserSchema) -> ReadUserSchema:
        with open("db_2.json") as file:
            db = json.load(file)
        id_max = 1
        for db_user in db:
            if user.nickname == db_user["nickname"]:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Такой никнейм уже есть")
            if id_max < db_user["id"]:
                id_max = db_user["id"]
        salt = "".join(choices(ascii_letters, k=16))
        user_dict = {
            "id": id_max+1,
            "nickname": user.nickname,
            "password_hash": self.get_hash(user.password, salt),
            "password_salt": salt,
            "data": user.data,
        }
        db.append(user_dict)
        with open("db_2.json", "w") as f:
            json.dump(db, f, indent=4)
        return user_dict


@router.get("/test_auth_2", status_code=status.HTTP_200_OK)
async def test_auth_2(
    credentials: HTTPBasicCredentials = Depends(get_credentials),
    repository: UserRepository = Depends(),
) -> ReadUserSchema:
    return repository.get_user(credentials.username, credentials.password)

@router.get("/", status_code=status.HTTP_200_OK)  # заменяет определение экземпляра класса
async def get_users(repository: UserRepository = Depends()) -> list[ReadUserSchema]:
    return repository.get_users()


@router.get("/{user_id}", status_code=status.HTTP_200_OK)  # получает пользователя по id
async def get_user_by_id(user_id: int, repository: UserRepository = Depends()) -> ReadUserSchema:
    user = repository.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого id не существует")
    return user

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: CreateUserSchema, repository: UserRepository = Depends()) -> ReadUserSchema:
    return repository.create_user(user)



