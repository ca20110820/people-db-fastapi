from typing import List, Union
from fastapi import FastAPI, Query
from pydantic import BaseModel
from app.crud import PeopleDB, DB_PATH
from app.model import Person


people_db = PeopleDB()


app = FastAPI(
    debug=True,
    title='Person DB',
    version="0.1.0"
)


class PersonList(BaseModel):
    data: List[Person]


@app.get("/")
async def read_root():
    return {
        "message": "Welcome to Person Database!"
    }


@app.get("/people/", response_model=List[dict])
async def get_people():
    global people_db
    result = [person.to_dict() for person in people_db.get_people()]
    return result


@app.get("/people/{person_id}", response_model=Union[Person, dict])
async def get_person(person_id: str):
    global people_db
    try:
        return people_db.get_person(person_id)
    except ValueError:
        return {
            "message": f"Person Not Found with id {person_id}."
        }
    except KeyError:
        return {
            "message": f"Person Not Found with id {person_id}."
        }


@app.post('/people/')
async def create_person(person_dict: dict):
    global people_db
    people_db.insert_person(person_dict)
    return {"ok": True}


@app.put('/people/')
async def update_person(person: Person):
    global people_db
    people_db.upsert_person(person)
    return {"ok": True}


@app.delete("/people/{person_id}")
async def delete_person(person_id: str):
    global people_db
    people_db.delete_person_by_id(person_id)
    return {"ok": True}
