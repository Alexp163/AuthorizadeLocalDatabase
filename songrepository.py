from pydantic import BaseModel
import json


class CreateSongSchema(BaseModel):
    name: str 
    data: str 


class ReadSongSchema(BaseModel):
    id: int 
    name: str 
    data: str 



class UpdateSongSchema(BaseModel):
    name: str 
    data: str 



class SongRepository:
    
    def create_song(self, song: CreateSongSchema) -> ReadSongSchema:  # добавить музыку
        with open("db_song.json") as file:
            db = json.load(file)
        id_max =1
        for db_song in db:
            if id_max < db_song["id"]:
                id_max = db_song["id"]
        song_dict = {
            "id": id_max+1,
            "name": song.name,
            "data": song.data,
        }
        db.append(song_dict)
        with open("db_song.json", "w") as f:
            json.dump(db, f, indent=4)
        return song_dict
    

    def get_song_by_id(self, song_id: int) -> ReadSongSchema:  # найти музыку по id
        with open("db_song.json") as file:
            db = json.load(file)
        for song in db:
            if song_id == song["id"]:
                return song 
        return None 
        
    def get_songs(self) -> list[ReadSongSchema]:  # список композиций
        with open("db_song.json") as file:
            db = json.load(file)
            return db

    def delete_song_by_id(self, song_id: int) -> None:  # удалить музыку по id
        with open("db_song.json") as file:
            db = json.load(file)
        for song in db:
            if song_id == song["id"]:
                db.remove(song) 
        with open("db_song.json", "w") as file:
            json.dump(db, file, indent=4)      
        return None
    
    def update_song_by_id(self, song_id: int, song: UpdateSongSchema) -> ReadSongSchema:  # обновить музыку
        with open("db_song.json") as file:
            db = json.load(file)
        
        for db_song in db:
            if  song_id == db_song["id"]:
                db_song["name"]  = song.name
                db_song["data"] = song.data
                with open("db_song.json", "w") as file:
                    json.dump(db, file, indent=4) 
                return db_song
        return None

    








