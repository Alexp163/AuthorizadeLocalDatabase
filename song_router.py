from fastapi import APIRouter, status, Depends
from songrepository import CreateSongSchema, SongRepository, ReadSongSchema, UpdateSongSchema
from fastapi.exceptions import HTTPException


router = APIRouter(tags=["song"], prefix="/song")


@router.post("/", status_code=status.HTTP_201_CREATED)  # добавить музыку
async def register(song: CreateSongSchema, repository: SongRepository = Depends()) -> ReadSongSchema:
    return repository.create_song(song)


@router.get("/{song_id}", status_code=status.HTTP_200_OK)  # найти музыку по id
async def get_song_by_id(song_id: int, repository: SongRepository = Depends()) -> ReadSongSchema:
    song = repository.get_song_by_id(song_id)
    if song is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого id не существует")
    return song 

@router.get("/", status_code=status.HTTP_200_OK)  # список композиций
async def get_songs(repository: SongRepository = Depends()) -> list[ReadSongSchema]:
    return repository.get_songs()

@router.delete("/{song_id}", status_code=status.HTTP_204_NO_CONTENT)  # удаление композиции
async def delete_song_by_id(song_id: int, repository: SongRepository = Depends()) -> None:
    song = repository.delete_song_by_id(song_id)


@router.put("/{song_id}", status_code=status.HTTP_200_OK)  # редактирование композиции
async def update_song_by_id(song_id: int, song: UpdateSongSchema,  repository: SongRepository = Depends()) -> ReadSongSchema:
    song_update = repository.update_song_by_id(song_id, song)
    if song_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого id не существует")
    return song_update



    