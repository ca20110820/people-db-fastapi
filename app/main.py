from fastapi import FastAPI, Query, Depends
from fastapi import HTTPException, status
from fastapi.responses import HTMLResponse
from typing import List, Union, Optional
from uuid import UUID
from app.crud import PeopleDB
from app.model import Person, create_flat_dct_from_person, create_person_from_dict


def get_db():
    return PeopleDB()


app = FastAPI(
    debug=True,
    title='Person DB',
    version="0.1.0"
)


HTML_HOME = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Person API</title>
</head>
<body>
    <header>
        <h1>Welcome to Person API</h1>
    </header>
    
    <main>
        I am only using this to practice API Development.
    </main>
    
    <footer>
        <p>&copy; 2024 Cedric Anover. All rights reserved.</p>
    </footer>

</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def read_root():
    return HTML_HOME


@app.get("/people", response_model=List[Person])
async def get_people(people_db: PeopleDB = Depends(get_db)):
    # result = [create_flat_dct_from_person(person) for person in people_db.get_people()]
    return people_db.get_people()


@app.get("/people/{person_id}", response_model=Person)
async def get_person(person_id: str, people_db: PeopleDB = Depends(get_db)):
    try:
        person = people_db.get_person(person_id)
        if not person:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Person Not Found with id {person_id}.")
        # return create_flat_dct_from_person(person)
        return person
    except (ValueError, KeyError) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@app.post('/people')
async def create_person(name: str,
                        dob: str,
                        occupation: Optional[str] = None,
                        height: Optional[Union[float, int]] = None,
                        people_db: PeopleDB = Depends(get_db)
                        ):
    person_dict = {
        "name": name,
        "dob": dob,
        "occupation": occupation,
        "height": height
    }
    person = Person.model_validate(person_dict)
    people_db.insert_person(person)


@app.put('/people/{person_id}')
async def update_person(person_id: str | UUID, person_dict: dict, people_db: PeopleDB = Depends(get_db)):
    people_db.upsert_person(person_id, person_dict)


@app.delete("/people/{person_id}")
async def delete_person(person_id: str | UUID, people_db: PeopleDB = Depends(get_db)):
    people_db.delete_person_by_id(str(person_id))
