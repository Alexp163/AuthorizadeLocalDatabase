from pydantic import BaseModel
import json

class CreateInstrumentSchema(BaseModel):
    title: str
    description: str

class ReadInstrumentSchema(BaseModel):
    id: int
    title: str 
    description: str 

class UpdateInstrumentSchema(BaseModel):
    title: str 
    description: str 


class InstrumentRepository:

    def create_instrument(self, instrument: CreateInstrumentSchema) -> ReadInstrumentSchema:  # добавить инструмент
        with open("db_instrument.json") as file:
            db = json.load(file)
        id_max = 1
        for db_instrument in db:
            if id_max < db_instrument["id"]:
                id_max = db_instrument["id"]
        instrument_dict = {
            "id": id_max+1,
            "title": instrument.title,
            "description": instrument.description,
        }
        db.append(instrument_dict)
        with open("db_instrument.json", "w") as file:
            json.dump(db, file, indent=4)
        return instrument_dict
    
    def get_instrument_by_id(self, instrument_id: int) -> ReadInstrumentSchema:  # найти инструмент по id
        with open("db_instrument.json") as file:
            db = json.load(file)
        for instrument in db:
            if instrument_id == instrument["id"]:
                return instrument 
        return None 
    
    def get_instruments(self) -> list[ReadInstrumentSchema]:  # все инструменты
        with open("db_instrument.json") as file:
            db = json.load(file)
            return db 
        
    def delete_instrument_by_id(self, instrument_id: int) -> None:  # удалить инструмент по id
        with open("db_instrument.json") as file:
            db = json.load(file)
        for instrument in db:
            if instrument_id == instrument["id"]:
                db.remove(instrument)
        with open("db_instrument.json", "w") as file:
            json.dump(db, file, indent=4)
        return None
    def update_instrument_by_id(self, instrument_id: int, instrument: UpdateInstrumentSchema) -> ReadInstrumentSchema:
        with open("db_instrument.json") as file:
            db = json.load(file)
        
        for db_instrument in db:
            if instrument_id == db_instrument["id"]:
                db_instrument["title"] = instrument.title
                db_instrument["description"] = instrument.description
                with open("db_instrument.json", "w") as file:
                    json.dump(db, file, indent=4)
                return db_instrument 
        return db_instrument 
    
    
    


