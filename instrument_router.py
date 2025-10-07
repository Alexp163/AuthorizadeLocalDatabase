from fastapi import APIRouter, status, Depends
from instrument_repository import CreateInstrumentSchema, ReadInstrumentSchema, UpdateInstrumentSchema, InstrumentRepository
from fastapi.exceptions import HTTPException


router = APIRouter(tags=["instrument"], prefix="/instrument")

@router.post("/", status_code=status.HTTP_201_CREATED)  # добавить инструмент
async def create_instrument(instrument: CreateInstrumentSchema, repository: InstrumentRepository = Depends()):
    return repository.create_instrument(instrument)

@router.get("/{instrument_id}", status_code=status.HTTP_200_OK)  # найти инструмент по id
async def get_instrument_by_id(instrument_id: int, repository: InstrumentRepository = Depends()) -> ReadInstrumentSchema:
    instrument = repository.get_instrument_by_id(instrument_id)
    if instrument is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого id не существует")
    return instrument 

@router.get("/", status_code=status.HTTP_200_OK)  # вывести списком все инструменты
async def get_instruments(repository: InstrumentRepository = Depends()) -> list[ReadInstrumentSchema]:
    return repository.get_instruments()

@router.delete("/{instrument_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_instrument_by_id(instrument_id: int, repository: InstrumentRepository = Depends()) -> None:
    instrument = repository.delete_instrument_by_id(instrument_id)

@router.put("/{instrument_id}", status_code=status.HTTP_200_OK)
async def update_instrument_by_id(instrument_id: int, instrument: UpdateInstrumentSchema, 
                                  repository: InstrumentRepository = Depends()) -> ReadInstrumentSchema:
    instrument_update = repository.update_instrument_by_id(instrument_id, instrument)
    if instrument_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого id не существует")
    return instrument_update 


