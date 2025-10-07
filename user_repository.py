from pydantic import BaseModel
import json
import hashlib
from fastapi.exceptions import HTTPException
from fastapi import status
from random import choices 
from string import ascii_letters


class UserCreateSchema(BaseModel):
    nickname: str 
    password: str 
    data: str 


class UserReadSchema(BaseModel):
    nickname: str 
    data: str



class UserRepository:
    def get_hash(self, password: str, salt: str) -> str:
        password_hash = hashlib.sha256(password.encode() +salt.encode()).hexdigest()
        return password_hash
    
    def get_users(self) -> list[UserReadSchema]:
        with open("db_user.json") as file:
            db = json.load(file)
        return db 


    def get_user(self, nickname: str, password: str) -> UserReadSchema:
        users = self.get_users()
        for user in users:
            if nickname == user["nickname"]:
                print("Имена совпали")
                if self.get_hash(password, user["password_salt"]) == user["password_hash"]:
                    print(f"{"Поздравляю, вы вошли в систему как "} - {nickname}")
                    return user 
                else:
                    print("Пароли не совпали")
        print("Совпадений нет!")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не найден")


    def create_user(self, user: UserCreateSchema) -> UserReadSchema:
        with open("db_user.json") as file:
            db = json.load(file)
        id_max = 1
        for db_user in db:
            if user.nickname == db_user["nickname"]:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Такой никнэйм уже есть")
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
        with open("db_user.json", "w") as file:
            json.dump(db, file, indent=4)
        return user_dict

    def get_data_by_username(self, username: str) -> str:
        with open("db_user.json") as file:
            db = json.load(file)
        for db_user in db:
            if db_user["nickname"] == username:
                return db_user["data"]
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Ничего не найдено")
