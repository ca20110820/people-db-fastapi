from typing import List
from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def read_root():
    return {
        "message": "Welcome to Person Database!"
    }


@app.get("/people/{person_id}")
async def get_person(person_id: str):
    # GET
    ...


async def create_person():
    # PUT
    ...


async def upsert_person():
    # UPDATE (OR CREATE if does not exist)
    ...


async def delete_person():
    # UPDATE (OR CREATE if does not exist)
    ...


@app.get("/people", response_model=List[dict])
async def get_people():
    # GET all collection of people
    ...
