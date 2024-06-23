from typing import List
from uuid import UUID
from pathlib import Path
from tinydb import TinyDB, Query


try:
    from app.model import Person, create_flat_dct_from_person, create_person_from_dict
except ModuleNotFoundError:
    from model import Person, create_flat_dct_from_person, create_person_from_dict


DB_PATH = Path(__file__).resolve().parent / 'data' / 'people.json'


class PeopleDB:
    def __init__(self):
        self.db_path = str(DB_PATH)

    def get_people(self) -> List[Person]:
        with TinyDB(self.db_path) as db:
            return [create_person_from_dict(person_dict) for person_dict in db.all()]

    def get_person(self, person_id: str) -> Person:
        with TinyDB(self.db_path) as db:
            person_dict = db.get(Query().person_id == person_id)
        return create_person_from_dict(person_dict)

    def insert_person(self, new_person: str | dict | Person) -> None:
        # Note: We assume that new_person_dict does not have 'person_id'
        with TinyDB(self.db_path) as db:
            if isinstance(new_person, dict):  # Assumed to be a Flat Dictionary (to be Serializable)
                Person.model_validate(new_person)  # Validatation
                db.insert(new_person)
            elif isinstance(new_person, str):  # Assumed to be JSON String
                person = Person.model_validate_json(new_person)
                dct = create_flat_dct_from_person(person)
                db.insert(dct)
            elif isinstance(new_person, Person):
                db.insert(create_flat_dct_from_person(new_person))

    def upsert_person(self, person_id: UUID | str, updated_properties: dict) -> None:
        # Assumption: updated_properties is a flat & serializable Python Dictionary
        # assert updated_properties['person_id'] == str(person_id), f"Person ID ({person_id}) is Invalid"
        with TinyDB(self.db_path) as db:
            db.upsert(updated_properties, Query().person_id == person_id)

    def delete_person(self, person: Person) -> None:
        with TinyDB(self.db_path) as db:
            db.remove(Query().person_id == str(person.person_id))

    def delete_person_by_id(self, person_id: str) -> None:
        with TinyDB(self.db_path) as db:
            db.remove(Query().person_id == person_id)
